import java.util.ArrayList;
import java.io.File;
import java.util.Scanner;
import java.lang.Double;

public class Write {
    public static boolean writeCleanFile(ArrayList<Integer> toRemove, String filename) {
        File file = new File(filename);
        ArrayList<String> lines = new ArrayList<String>();

        try (Scanner input = new Scanner(file)) {
            while (input.hasNextLine()) {
                String line = input.nextLine();
                line = line.replace("\n", "").replace("\r", "");
                lines.add(line);
            }
        } catch (java.io.FileNotFoundException e) {
            System.out.println("There was an error with opening the file:");
            System.out.println(e);
	    return false;
        }
	add1(toRemove);
	printArrayList(lines);
	removeLines(lines, toRemove);
	printArrayList(lines);
	return true;
    }
    /**
     * This method is needed because the toRemove indexes are based on just the data, and
     * doesn't include the header line at the first line.
    */
    private static void add1(ArrayList<Integer> toRemove) {
	for (int i = 0; i < toRemove.size(); i++) {
	    toRemove.set(i, toRemove.get(i) + 1);
	}
    }
    private static void removeLines(ArrayList<String> lines, ArrayList<Integer> removeList) {
	for (int i = removeList.size() - 1; i > -1; i--) {
	    int index = removeList.get(i);
	    lines.remove(index);
	}
    }
    private static <E> void printArrayList(ArrayList<E> input) {
	for (E val : input) {
	    System.out.println(val);
	}
	System.out.println();
    }
}
