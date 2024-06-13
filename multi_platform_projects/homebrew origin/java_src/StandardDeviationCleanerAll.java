import java.util.ArrayList;
public class StandardDeviationCleanerAll extends StandardDeviationCleaner {
    public ArrayList<Integer> runCleaningAlgorithm(ArrayList<ArrayList<Double>> data, ArrayList<Integer> alreadyRemoved) {
	ArrayList<Integer> p12ToRemove = getToRemove(data.get(4), alreadyRemoved);  // 4 is the P12 col index
	ArrayList<Integer> p14ToRemove = getToRemove(data.get(5), alreadyRemoved);  // 5 is the P14 col index
	ArrayList<Integer> bgToRemove = getToRemove(data.get(6), alreadyRemoved);  // 6 is the BG col index

	ArrayList<Integer> combinedToRemove = combineToRemove(p12ToRemove, p14ToRemove, bgToRemove);
	return combinedToRemove;
    }
    private ArrayList<Integer> combineToRemove(ArrayList<Integer> toRemove1, ArrayList<Integer> toRemove2, ArrayList<Integer> toRemove3) {
	ArrayList<Integer> toRemoveOutput = toRemove1;
	for (Integer val : toRemove2) {
	    if (! toRemoveOutput.contains(val)) insertIndex(toRemoveOutput, val);
	}
	for (Integer val : toRemove3) {
	    if (! toRemoveOutput.contains(val)) insertIndex(toRemoveOutput, val);
	}
	return toRemoveOutput;
    }
    private void insertIndex(ArrayList<Integer> toRemove, Integer val) {
	int addIndex = -1;
	for (int i = 0; i < toRemove.size(); i++) {
	    if (toRemove.get(i) > val) {
		addIndex = i;
		break;
	    }
	}
	toRemove.add(addIndex, val);
    }
}
