import java.util.ArrayList;
public class CloudCleaner extends AbstractCleaner {
    public ArrayList<Integer> runCleaningAlgorithm(ArrayList<ArrayList<Double>> data, ArrayList<Integer> alreadyRemoved) {
	System.out.println("Running Cloud Cleaning Algorithm (STDEV cleaning on the OHTemp Residual analysis graph)");
	ArrayList<Double> timeData = data.get(0);
	ArrayList<Double> tempData = data.get(1);

	Graph inputGraph = new Graph(timeData, tempData);
	Graph residualGraph = getResidualAnalysisGraph(inputGraph, alreadyRemoved);
	ArrayList<Integer> toRemove = cleanResidual(residualGraph, alreadyRemoved, timeData);
	printArrayList(toRemove);

	return toRemove;
    }
    private ArrayList<Integer> cleanResidual(Graph residualGraph, ArrayList<Integer> alreadyRemoved, ArrayList<Double> allTime) {
	ArrayList<Double> smoothRemoved = residualGraph.getXData();
	ArrayList<Double> residualData = residualGraph.getYData();

	// Temporarily merge the removed into a new list so that they'll work with the STDEV functions
	
	double mean = STDEV.getMean(residualData, new ArrayList<Integer>());
	double standardDev = STDEV.getStdDev(residualData, mean, new ArrayList<Integer>());
	System.out.printf("Mean: %f\nStandardDeviation: %f\n\n", mean, standardDev);
	double upperBound = mean + (2 * standardDev);
	double lowerBound = mean - (2 * standardDev);

	ArrayList<Integer> toRemove = new ArrayList<Integer>();
	int resDataIndex = 0;
	for (int i = 0; i < allTime.size(); i++) {
	    if (alreadyRemoved.contains(i)) continue;
	    else if (smoothRemoved.contains(allTime.get(i))) {
		toRemove.add(i);  // Adding smoothRemoved to toRemoved w/o using residual data
		continue;
	    } else {
	        double val = residualData.get(resDataIndex);
	        resDataIndex++;
	        if (val > upperBound || val < lowerBound) {
	       	    toRemove.add(i);
	        }
	    }
	}

	return toRemove;
    }

    private Graph getResidualAnalysisGraph(Graph inputData, ArrayList<Integer> alreadyRemoved) {
	Graph smoothedLine = getSmoothedLine(inputData, alreadyRemoved);
	//printGraph(smoothedLine);

	ArrayList<Double> allTime = inputData.getXData();
	ArrayList<Double> allTemp = inputData.getYData();
	ArrayList<Double> smoothRemoved = smoothedLine.getXData();
	ArrayList<Double> smoothTemp = smoothedLine.getYData();

	ArrayList<Double> residualData = makeResidualData(allTemp, smoothTemp, allTime, alreadyRemoved, smoothRemoved);
	//printArrayList(residualData);
	Graph ResidualAnalysisGraph = new Graph(smoothRemoved, residualData);
	return ResidualAnalysisGraph;

	// TODO: Make sure that null objects are accounted for (probably removed).
    }
    private ArrayList<Double> makeResidualData(ArrayList<Double> allTemp, ArrayList<Double> smoothedTemp, ArrayList<Double> allTimes, ArrayList<Integer> alreadyRemoved, ArrayList<Double> smoothRemoved) {
	ArrayList<Double> residualData = new ArrayList<Double>();
	int smoothTempIndex = 0;
	for (int i = 0; i < allTimes.size(); i++) {
	    if (alreadyRemoved.contains(i) || smoothRemoved.contains(allTimes.get(i))) continue;
	    double rawTemp = allTemp.get(i);
	    double smoothTemp = smoothedTemp.get(smoothTempIndex);
	    smoothTempIndex++;
	    double residualTemp = rawTemp - smoothTemp;
	    residualData.add(residualTemp);
	}
	return residualData;
    }
    private Graph getSmoothedLine(Graph inputData, ArrayList<Integer> alreadyRemoved) {
	int i = 0;
	ArrayList<Double> movingAverages = new ArrayList<Double>();
	int windowSize = 9; // Make sure it's odd so the number removed from each side is the same. Makes accurate time adjustment easy.
	int lenRemovedFromEachSide = windowSize / 2;
	ArrayList<Double> inputTime = inputData.getXData();
	ArrayList<Double> inputTemp = inputData.getYData();

	// Since it's hard to know how many indexes are alreadyRemoved, letting the exception handling break the loop
	while (true) {
	    if (alreadyRemoved.contains(i)) {i++; continue;}
	    try {
		double windowSum = getWindowSum(windowSize, i, inputTemp, alreadyRemoved);
		double windowAvg = windowSum / windowSize;
		movingAverages.add(windowAvg);
	    } catch (IndexOutOfBoundsException ex) {
		break;  // There are no more values that aren't already removed.
	    }
	    i++;
	}
	ArrayList<Double> timesRemovedBySmoothing = getTimeValsRemovedBySmoothing(inputTime, lenRemovedFromEachSide, alreadyRemoved);

	// Misusing Graph() slightly to return times removed so the caller can deal with accounting for alreadyRemoved.
	return new Graph(timesRemovedBySmoothing, movingAverages);
    }
    private ArrayList<Double> getTimeValsRemovedBySmoothing(ArrayList<Double> inputTime, int lenRemovedFromEachSide, ArrayList<Integer> alreadyRemoved) {
	ArrayList<Double> output = new ArrayList<Double>();

	int removeFromStart = lenRemovedFromEachSide;
	int removeFromEnd = lenRemovedFromEachSide;

	for (int i = 0; i < inputTime.size() && removeFromStart > 0; i++) {
	    if (alreadyRemoved.contains(i)) continue;
	    output.add(inputTime.get(i));
	    removeFromStart -= 1;
	}
	for (int i = inputTime.size() - 1; i >= 0 && removeFromEnd > 0; i--) {
	    if (alreadyRemoved.contains(i)) continue;
	    output.add(inputTime.get(i));
	    removeFromEnd -= 1;
	}
	return output;
    }
    private double getWindowSum(int windowSize, int startIndex, ArrayList<Double> data, ArrayList<Integer> alreadyRemoved) throws IndexOutOfBoundsException {
	double sum = 0;
	int valuesAdded = 0;
	int i = startIndex;
	while (valuesAdded < windowSize) {
	    if (alreadyRemoved.contains(i)) {i++; continue;}
	    sum += data.get(i);
	    valuesAdded++;
	    i++;
	}
	return sum;
    }
    private <E> void printArrayList(ArrayList<E> input) {
	for (E val : input) {
	    System.out.println(val);
	}
	System.out.println();
    }


    private class Graph {
	private ArrayList<Double> xData;
	private ArrayList<Double> yData;

	public Graph(ArrayList<Double> xInput, ArrayList<Double> yInput) {
	    this.xData = xInput;
	    this.yData = yInput;
	}
	public ArrayList<Double> getXData() {
	    return copyArrayList(xData);
	}
	public ArrayList<Double> getYData() {
	    return copyArrayList(yData);
	}
	private ArrayList<Double> copyArrayList(ArrayList<Double> input) {
	    ArrayList<Double> output = new ArrayList<Double>();
	    for (Double val : input) {
		output.add(val);
	    }
	    return output;
	}
    }
    private void printGraph(Graph graph) {
	ArrayList<Double> xData = graph.getXData();
	ArrayList<Double> yData = graph.getYData();
	System.out.println("X-Data:");
	printArrayList(xData);
	System.out.println("Y-Data:");
	printArrayList(yData);
    }
}
