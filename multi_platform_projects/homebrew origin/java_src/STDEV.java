import java.util.ArrayList;
public class STDEV {
    public double getMean(ArrayList<Double> column, ArrayList<Integer> alreadyRemoved) {
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
    public double getStdDev(ArrayList<Double> column, double mean, ArrayList<Integer> alreadyRemoved) {
        double errorSum = getErrorSum(column, mean, alreadyRemoved);
	int valCount = column.size() - alreadyRemoved.size();
	double stdDev = java.lang.Math.sqrt(errorSum / (valCount - 1));
	return stdDev;
    }
    public double getStdDev(ArrayList<Double> column, double mean, ArrayList<Integer> alreadyRemoved) {
        double errorSum = getErrorSum(column, mean, alreadyRemoved);
	int valCount = column.size() - alreadyRemoved.size();
	double stdDev = java.lang.Math.sqrt(errorSum / (valCount - 1));
	return stdDev;
    }
}
