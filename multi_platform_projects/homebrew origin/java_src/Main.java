import java.util.ArrayList;
import java.lang.Double;

public class Main {
    public static void main(String[] args) {
        String filename = args[0];
        ArrayList<ArrayList<Double>> inData = Parser.parseFile(filename);
        
	ArrayList<Integer> removeIndexesMain = new ArrayList<Integer>();
	ArrayList<Integer> removeIndexesTemp;

        AbstractCleaner cleaner1 = new StandardDeviationCleanerBGOnly();
	removeIndexesTemp = cleaner1.runCleaningAlgorithm(inData, removeIndexesMain);
	removeIndexesMain = combineToRemove(removeIndexesTemp, removeIndexesMain);

	AbstractCleaner cleaner2 = new PreOHCleaner();
	removeIndexesTemp = cleaner2.runCleaningAlgorithm(inData, removeIndexesMain);
	removeIndexesMain = combineToRemove(removeIndexesTemp, removeIndexesMain);

	AbstractCleaner cleaner3 = new CloudCleaner();
	removeIndexesTemp = cleaner3.runCleaningAlgorithm(inData, removeIndexesMain);
	removeIndexesMain = combineToRemove(removeIndexesTemp, removeIndexesMain);

	String write_file = Write.writeCleanFile(removeIndexesMain, filename);

	if (write_file != "") {
	    System.out.printf("The cleaned file was successfully written to \"%s\" with %d lines removed.\n\n", write_file, removeIndexesMain.size());
	    System.out.println("The following line indexes were removed from the original file:");
	    printArrayList(removeIndexesMain);
	}
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
    private static ArrayList<Integer> combineToRemove(ArrayList<Integer> toRemove1, ArrayList<Integer> toRemove2) {
	ArrayList<Integer> toRemoveOutput = toRemove1;
	for (Integer val : toRemove2) {
	    if (! toRemoveOutput.contains(val)) toRemoveOutput.add(val);
	}
	return toRemoveOutput;
    }
}
