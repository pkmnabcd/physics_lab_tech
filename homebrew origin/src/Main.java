import java.io.File;
import java.util.Scanner;
import java.util.ArrayList;

public class Main {
    public static void main(String[] args) {
        File file = new File("");
        try (Scanner input = new Scanner(file)) {
            if (input.hasNextLine()) {
                input.nextLine();
            }
        } catch (java.io.FileNotFoundException e) {
            System.out.println("There was an error with opening the file:");
            System.out.println(e);
            System.exit(1);
        }
    }
}