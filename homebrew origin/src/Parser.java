import java.util.ArrayList;
import java.io.File;
import java.util.Scanner;
import java.lang.Double;

public class Parser {
    /**
     * This reads the data from the given file. If invalid data is given, null object is used instead of a Double object in that position in the output data.
     *  @param filename the path to and the name of the file that you want read.
     */
    public static ArrayList<Double> parseFile(String filename) {
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
        
        String header_line = lines.remove(0);
	int line_len = header_line.length();
	int col_len = 15;

	return new ArrayList<Double>();
    }
}
