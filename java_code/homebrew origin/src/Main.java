import java.util.ArrayList;
import java.lang.Double;

public class Main {
    public static void main(String[] args) {
        String filename = args[0];
        ArrayList<ArrayList<Double>> inData = Parser.parseFile(filename);
        
        AbstractCleaner cleaner = new StandardDeviationCleaner();
	cleaner.runCleaningAlgorithm(inData);
	printInput(inData);
    }
    private static void printInput(ArrayList<ArrayList<Double>> inArray) {
	for (ArrayList<Double> col : inArray) {
	    for (Double val : col) {
	        System.out.print(val);
		System.out.print(" ");
	    }
	    System.out.println();
	}
    }
}
