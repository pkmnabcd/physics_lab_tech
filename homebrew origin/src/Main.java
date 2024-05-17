import java.io.File;
import java.util.Scanner;
import java.util.ArrayList;

public class Main {
    public static void main(String[] args) {
	    String filename = args[0];
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
        for (String line : lines) {
            System.out.println(line);
        }
    }
}