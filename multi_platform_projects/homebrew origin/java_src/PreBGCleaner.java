import java.util.ArrayList;

public class PreBGCleaner extends AbstractCleaner {
    public ArrayList<Integer> runCleaningAlgorithm(ArrayList<ArrayList<Double>> data, ArrayList<Integer> alreadyRemoved) {
	ArrayList<Double> BGData = data.get(6);
	ArrayList<Integer> toRemove = new ArrayList<Integer>();
	for (int i = 0; i < BGData.size(); i++) {
	    if (alreadyRemoved.contains(i)) continue;
	    if (BGData.get(i) == null) toRemove.add(i);
	}
	return toRemove;
    }
}
