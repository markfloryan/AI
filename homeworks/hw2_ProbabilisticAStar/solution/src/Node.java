import java.awt.Point;


public class Node{

	public int distToNode = -1;
	public double heuristic = -1;
	public Point position;
	public Node previous = null;

	public Node(Point pos, int dist, double heuristic){
		this.position = pos;
		this.distToNode = dist;
		this.heuristic = heuristic;
	}

	public double totalCost(){
		return (double)distToNode + heuristic;
	}

	@Override
	public boolean equals(Object obj){
		Node other = (Node)obj;

		if(position.x==other.position.x && position.y==other.position.y)
			return true;

		return false;
	}

	public String toString(){
		return "[Node] position: " + position + "; dist: " + distToNode + "; h: " + heuristic + "; previous is null? " + (previous == null);
	}

}
