import java.util.ArrayList;
public class StandardDeviationCleanerBGOnly extends StandardDeviationCleaner {
    public ArrayList<Integer> runCleaningAlgorithm(ArrayList<ArrayList<Double>> data, ArrayList<Integer> alreadyRemoved) {
	System.out.println("Running STDEV cleaning on BG filter");
	ArrayList<Integer> bgToRemove = getToRemove(data.get(6), alreadyRemoved);  // 6 is the BG col index

	return bgToRemove;
    }
    @Override
    protected ArrayList<Integer> getIndexesToRemove(ArrayList<Double> column, double mean, double stdDev, ArrayList<Integer> alreadyRemoved) {
	double upperLimit;
	double lowerLimit;
	boolean twilightAtStart = twilightAtBeginning(column);
	boolean twilightAtFinish = twilightAtEnd(column);
	if (twilightAtStart && twilightAtFinish) {
	    System.out.println("Aggressive bounds used.");
	    upperLimit = mean + (0.18 * stdDev);
	    lowerLimit = mean - stdDev;
	} else if (twilightAtStart || twilightAtFinish) {
	    System.out.println("Medium aggressive bounds used.");
	    upperLimit = mean + (0.5 * stdDev);
	    lowerLimit = mean - stdDev;
	} else {
	    System.out.println("No twilight detected. Large bounds used.");
	    upperLimit = mean + (2 * stdDev);
	    lowerLimit = mean - (2 * stdDev);
	}
	System.out.printf("Upper Limit: %f\nLower Limit: %f\n\n", upperLimit, lowerLimit);
	ArrayList<Integer> indexes = new ArrayList<Integer>();
	for (int i = 0; i < column.size(); i++) {
	    if (alreadyRemoved.contains(i)) continue;
	    Double val = column.get(i);
	    if (val == null || (val > upperLimit || val < lowerLimit)) {
		indexes.add(i);
	    }
	}
	return indexes;
    }
    private boolean twilightAtBeginning(ArrayList<Double> column) {
	if (column.get(0) > 50000) {
	    System.out.println("Twilight detected at the beginning.");
	    return true;
	}
	return false;
    }
    private boolean twilightAtEnd(ArrayList<Double> column) {
	if (column.get(column.size() - 1) > 50000) {
	    System.out.println("Twilight detected at the end.");
	    return true;
	}
	return false;
    }
}
