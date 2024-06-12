import java.util.ArrayList;
public abstract class StandardDeviationCleaner extends AbstractCleaner {
    protected ArrayList<Integer> getToRemove(ArrayList<Double> column, ArrayList<Integer> alreadyRemoved) {
	double mean = getMean(column, alreadyRemoved);
	double stdDev = getStdDev(column, mean, alreadyRemoved);
	ArrayList<Integer> toRemove = getIndexesToRemove(column, mean, stdDev, alreadyRemoved);
	return toRemove;
    }
    protected double getMean(ArrayList<Double> column, ArrayList<Integer> alreadyRemoved) {
	int valCount = column.size();
	double total = 0;
        for (int i = 0; i < column.size(); i++) {
	    if (alreadyRemoved.contains(i)) {
		valCount--;
		continue;
	    }
	    double val = column.get(i);
	    total += val;
	}
	double mean = total / valCount;
	return mean;
    }
    private double getErrorSum(ArrayList<Double> column, double mean, ArrayList<Integer> alreadyRemoved) {
	double total = 0;
        for (int i = 0; i < column.size(); i++) {
	    if (alreadyRemoved.contains(i)) {
		continue;
	    }
	    double val = column.get(i);
	    total += java.lang.Math.pow((val - mean), 2);
	}
	return total;
    }
    protected double getStdDev(ArrayList<Double> column, double mean, ArrayList<Integer> alreadyRemoved) {
        double errorSum = getErrorSum(column, mean, alreadyRemoved);
	int valCount = column.size() - alreadyRemoved.size();
	double stdDev = java.lang.Math.sqrt(errorSum / (valCount - 1));
	return stdDev;
    }
    protected ArrayList<Integer> getIndexesToRemove(ArrayList<Double> column, double mean, double stdDev, ArrayList<Integer> alreadyRemoved) {
	double upperLimit = mean + stdDev;
	double lowerLimit = mean - stdDev;
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
