import java.util.ArrayList;
public class MiscTest {
    public static void main(String[] args) {
        AbstractCleaner cleaner = new CloudCleaner();

	ArrayList<ArrayList<Double>> inputData = new ArrayList<ArrayList<Double>>();
	inputData.add(new ArrayList<Double>());
	inputData.add(new ArrayList<Double>());
	for (ArrayList<Double> list : inputData) {
	    double addVal = 1.0;
	    for (int i = 0; i < 5; i++) {
		list.add(addVal);
		addVal++;
	    }
	}
	ArrayList<Integer> removeIndexesMain = new ArrayList<Integer>();

	ArrayList<Integer> removeIndexesTemp = cleaner.runCleaningAlgorithm(inputData, removeIndexesMain);
        
    }
}
