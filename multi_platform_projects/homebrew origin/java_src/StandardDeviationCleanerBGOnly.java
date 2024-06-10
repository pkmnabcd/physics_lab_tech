import java.util.ArrayList;
public class StandardDeviationCleanerBGOnly extends StandardDeviationCleaner {
    public ArrayList<Integer> runCleaningAlgorithm(ArrayList<ArrayList<Double>> data) {
	System.out.println("Running STDEV cleaning on BG filter");
	ArrayList<Integer> bgToRemove = getToRemove(data.get(6));  // 6 is the BG col index

	return bgToRemove;
    }
    @Override
    protected ArrayList<Integer> getIndexesToRemove(ArrayList<Double> column, double mean, double stdDev) {
	double upperLimit = mean;
	double lowerLimit = mean - stdDev;
	System.out.printf("Upper Limit: %f\nLower Limit: %f\n\n", upperLimit, lowerLimit);
	ArrayList<Integer> indexes = new ArrayList<Integer>();
	for (int i = 0; i < column.size(); i++) {
	    Double val = column.get(i);
	    if (val == null || (val > upperLimit || val < lowerLimit)) {
		indexes.add(i);
	    }
	}
	return indexes;
    }
}