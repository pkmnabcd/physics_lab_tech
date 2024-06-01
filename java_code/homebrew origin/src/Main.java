import java.util.ArrayList;
import java.lang.Double;

public class Main {
    public static void main(String[] args) {
        String filename = args[0];
        ArrayList<ArrayList<Double>> inData = Parser.parseFile(filename);
        
        AbstractCleaner cleaner = new StandardDeviationCleaner();
	ArrayList<Integer> removeIndexes = cleaner.runCleaningAlgorithm(inData);
	printInput(inData);
	printArrayList(removeIndexes);
	boolean success = Write.writeCleanFile(removeIndexes, filename);
	if (success) System.out.println("The cleaned file was written");
    }
    private static void printInput(ArrayList<ArrayList<Double>> inArray) {
	for (ArrayList<Double> col : inArray) {
	    System.out.println(col.size());
	    for (Double val : col) {
	        System.out.print(val);
		System.out.print(" ");
	    }
	    System.out.println();
	}
	System.out.println();
    }
    private static <E> void printArrayList(ArrayList<E> input) {
	for (E val : input) {
	    System.out.println(val);
	}
	System.out.println();
    }
}
