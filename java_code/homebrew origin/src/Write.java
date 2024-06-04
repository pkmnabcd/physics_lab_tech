import java.util.ArrayList;
import java.io.File;
import java.util.Scanner;
import java.lang.Double;
import java.io.IOException;
import java.io.FileWriter;
import java.lang.StringBuilder;

public class Write {
    public static String writeCleanFile(ArrayList<Integer> toRemove, String filename) {
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
	    return "";
        }
	add1(toRemove);
	removeLines(lines, toRemove);
	filename = editFilename(filename);
	if (writeFile(lines, filename)) {
	    return filename;
	} else {
	    return "";
	}
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
    /**
     * This method adds e to the end of the filename before .dat to signify this is the
     * edited version of the input file.
    */
    private static String editFilename(String filename) {
	filename = filename.replaceFirst(".dat", "e.dat");
	return filename;
    }
    private static boolean writeFile(ArrayList<String> lines, String filename) {
	try {
	    File file = new File(filename);
	    file.createNewFile();
	    FileWriter writer = new FileWriter(filename);
	    String combinedLines = combineLines(lines);
	    writer.write(combinedLines);
	    writer.close();

	} catch (IOException e) {
	    System.out.println("An error occurred.");
	    e.printStackTrace();
	    return false;
	}
	return true;
    }
    private static String combineLines(ArrayList<String> lines) {
	StringBuilder outString = new StringBuilder();
	for (int i = 0; i < lines.size(); i++) {
	    String line = lines.get(i);
	    outString.append(line);
	    if (i != lines.size() - 1) {
	        outString.append("\n");
	    }
	}
	return outString.toString();
    }
}
