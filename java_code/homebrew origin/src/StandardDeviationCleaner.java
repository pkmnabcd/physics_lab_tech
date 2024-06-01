import java.util.ArrayList;
public class StandardDeviationCleaner extends AbstractCleaner {
    public ArrayList<Integer> runCleaningAlgorithm(ArrayList<ArrayList<Double>> data) {
	int index = 4;  // 4 is the P12 col index
	double mean = getMean(data.get(index));
	double stdDev = getStdDev(data.get(index), mean);
	ArrayList<Integer> toRemove = getIndexesToRemove(data.get(index), mean, stdDev);
	return toRemove;
    }
    private double getMean(ArrayList<Double> column) {
	int valCount = column.size();
	double total = 0;
        for (Double val : column) {
	    total += val.doubleValue();
	}
	double mean = total / valCount;
	return mean;
    }
    private double getErrorSum(ArrayList<Double> column, double mean) {
	double total = 0;
	for (Double val : column) {
	    total += java.lang.Math.pow((val - mean), 2);
	}
	return total;
    }
    private double getStdDev(ArrayList<Double> column, double mean) {
        double errorSum = getErrorSum(column, mean);
	int valCount = column.size();
	double stdDev = java.lang.Math.sqrt(errorSum / (valCount - 1));
	return stdDev;
    }
    private ArrayList<Integer> getIndexesToRemove(ArrayList<Double> column, double mean, double stdDev) {
	double upperLimit = mean + stdDev;
	double lowerLimit = mean - stdDev;
	ArrayList<Integer> indexes = new ArrayList<Integer>();
	for (int i = 0; i < column.size(); i++) {
	    Double val = column.get(i);
	    if (val == null || (val > upperLimit || val < lowerLimit)) {
		indexes.add(i);
	    }
	}
	return indexes;
    }
    private <E> void printArrayList(ArrayList<E> input) {
	for (E val : input) {
	    System.out.println(val);
	}
	System.out.println();
    }
    private <E> void print2DArrayList(ArrayList<ArrayList<E>> input) {
	for (ArrayList<E> innerArray : input) {
	    System.out.println(innerArray.size());
	    for (E val : innerArray) {
		System.out.printf("%s ", val);
	    }
	    System.out.println();
	}
	System.out.println();
    }
}
