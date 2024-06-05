import java.util.ArrayList;
public class StandardDeviationCleanerBGOnly extends StandardDeviationCleaner {
    public ArrayList<Integer> runCleaningAlgorithm(ArrayList<ArrayList<Double>> data) {
	ArrayList<Integer> p14ToRemove = getToRemove(data.get(5));  // 5 is the P14 col index

	return p14ToRemove;
    }
    @Override
    protected ArrayList<Integer> getIndexesToRemove(ArrayList<Double> column, double mean, double stdDev) {
	double upperLimit = mean + 2 * stdDev;
	double lowerLimit = mean + 2 * stdDev;
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
