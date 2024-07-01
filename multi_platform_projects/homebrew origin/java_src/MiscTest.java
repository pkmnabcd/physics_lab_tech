import java.util.ArrayList;
public class MiscTest {
    public static void main(String[] args) {
        AbstractCleaner cleaner = new CloudCleaner();

	ArrayList<ArrayList<Double>> inputData = new ArrayList<ArrayList<Double>>();
	inputData.add(new ArrayList<Double>());
	inputData.add(new ArrayList<Double>());
	for (ArrayList<Double> list : inputData) {
	    double addVal = 1.0;
	    for (int i = 0; i < 12; i++) {
		list.add(addVal);
		//addVal++;
	    }
	}
	for (ArrayList<Double> list : inputData) {
	    list.add(0, 21.0);
	    list.add(0, 20.0);
	    list.add(list.size(), 22.0);
	    list.add(list.size(), 23.0);
	    list.add(6, 19.0);
	    
	}
	printArrayList(inputData.get(0));
	printArrayList(inputData.get(1));

	ArrayList<Integer> removeIndexesMain = new ArrayList<Integer>();
	//removeIndexesMain.add(16);
	//removeIndexesMain.add(15);
	//removeIndexesMain.add(6);
	//removeIndexesMain.add(0);
	//removeIndexesMain.add(1);

	ArrayList<Integer> removeIndexesTemp = cleaner.runCleaningAlgorithm(inputData, removeIndexesMain);
        
    }
    private static <E> void printArrayList(ArrayList<E> input) {
	for (E val : input) {
	    System.out.println(val);
	}
	System.out.println();
    }
}
