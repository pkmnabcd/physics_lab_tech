import java.util.ArrayList;
import java.lang.Double;

public class Main {
    public static void main(String[] args) {
        String filename = args[0];
        ArrayList<ArrayList<Double>> inData = Parser.parseFile(filename);

	for (ArrayList<Double> col : inData) {
	    for (Double val : col) {
	        System.out.print(val);
		System.out.print(" ");
	    }
	    System.out.println();
	}
    }
}
