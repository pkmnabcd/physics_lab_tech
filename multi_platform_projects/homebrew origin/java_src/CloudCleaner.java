import java.util.ArrayList;
public class CloudCleaner extends AbstractCleaner {
    public ArrayList<Integer> runCleaningAlgorithm(ArrayList<ArrayList<Double>> data, ArrayList<Integer> alreadyRemoved) {
	ArrayList<Double> timeData = data.get(0);
	ArrayList<Double> tempData = data.get(1);

	Graph inputGraph = new Graph(timeData, tempData);
	Graph residualGraph = getResidualAnalysisGraph(inputGraph, alreadyRemoved);

	return new ArrayList<Integer>();
    }


    private Graph getResidualAnalysisGraph(Graph inputData, ArrayList<Integer> alreadyRemoved) {
	Graph smoothedLine = getSmoothedLine(inputData, alreadyRemoved);

	// TODO: Make sure that null objects are accounted for (probably removed).

	return new Graph(new ArrayList<Double>(), new ArrayList<Double>());
    }

    private Graph getSmoothedLine(Graph inputData, ArrayList<Integer> alreadyRemoved) {
	int i = 0;
	ArrayList<Double> movingAverages = new ArrayList<Double>();
	int windowSize = 9; // Make sure it's odd so the number removed from each side is the same. Makes accurate time adjustment easy.
	int lenRemovedFromEachSide = windowSize / 2;
	ArrayList<Double> inputTime = inputData.getXData();
	ArrayList<Double> inputTemp = inputData.getYData();

	while (i < inputTemp.size() - windowSize) {
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
}
