import java.util.ArrayList;

public class PreOHCleaner extends AbstractCleaner {
    public ArrayList<Integer> runCleaningAlgorithm(ArrayList<ArrayList<Double>> data, ArrayList<Integer> alreadyRemoved) {
	ArrayList<Double> OHData = data.get(1);
	ArrayList<Integer> toRemove = new ArrayList<Integer>();
	for (int i = 0; i < OHData.size(); i++) {
	    if (alreadyRemoved.contains(i)) continue;
	    if (OHData.get(i) == null) toRemove.add(i);
	    else if (OHData.get(i) > 250) toRemove.add(i);
	    else if (OHData.get(i) < 0) toRemove.add(i);
	}
	return toRemove;
    }
}
