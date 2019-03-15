import java.util.Comparator;

public class NodeComparator implements Comparator<Node>{


	@Override
	public int compare(Node o1, Node o2){
		if(o2.totalCost() - o1.totalCost() < 0) return 1;

		else if(o2.totalCost() == o1.totalCost()) return 0;

		return -1;
	}

}
