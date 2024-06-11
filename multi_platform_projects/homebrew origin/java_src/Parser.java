import java.util.ArrayList;
import java.io.File;
import java.util.Scanner;
import java.lang.Double;

public class Parser {
    /**
     * This reads the data from the given file. If invalid data is given, null object is used instead of a Double object in that position in the output data.
     *  @param filename the path to and the name of the file that you want read.
     *  @return 2D ArrayList<ArrayList<Double>> where each inner array has a column of data.
     */
    public static ArrayList<ArrayList<Double>> parseFile(String filename) {
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
            System.exit(1);
        }
        
        String headerLine = lines.remove(0);
	int lineLength = headerLine.length();
	int colLength = 15;
	int numberOfColumns = (int)(lineLength / colLength);
	ArrayList<ArrayList<Double>> rowSet = new ArrayList<ArrayList<Double>>();

	for (String line : lines) {
	    ArrayList<Double> lineData = new ArrayList<Double>();
	    for (int i = 0; i < numberOfColumns; i++) {
	        int indexStart = i * colLength;
		int indexEnd = indexStart + colLength;
		String substring = line.substring(indexStart, indexEnd);
		substring = substring.replace(" ", "");
		if (substring.contains("*")) {
		    lineData.add(null);
		} else if (substring.contains("NaN")) {
		    lineData.add(null);
		} else {
		    lineData.add(Double.valueOf(substring));
		}
            }
	    rowSet.add(lineData);
	}

        ArrayList<ArrayList<Double>> colSet = rowSetToColSet(rowSet);

	return colSet; 
    }
    public static ArrayList<ArrayList<Double>> rowSetToColSet(ArrayList<ArrayList<Double>> rowSet) {
        int rowCount = rowSet.size();
	int colCount = rowSet.get(0).size();
	ArrayList<ArrayList<Double>> colSet = new ArrayList<>();

	for (int j = 0; j < colCount; j++) {
	    colSet.add(new ArrayList<Double>());
	}
	for (int i = 0; i < rowCount; i++) {
	    for (int j = 0; j < colCount; j++) {
	        colSet.get(j).add(rowSet.get(i).get(j));
	    }
	}
	return colSet;
    }
}
