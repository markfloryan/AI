import java.awt.Point;

public class Node implements Comparable<Node> {
	// fields
	int x, y;
	Point p;
	String type;
	int cost = 999999999;
	Node parent;
	static Node dest = null;
	private boolean traversed;

	Node(int x, int y, String t) {
		this.x = x;
		this.y = y;
		p = new Point(x, y);
		this.type = t;
		traversed = false;

	}
	Node(int x, int y) {
		this.x = x;
		this.y = y;
		p = new Point(x, y);
		this.type = "O";
		traversed = false;

	}

	
	public int heuristic() {
		//return 0;
		return (int) Math.floor(Math.sqrt((x - dest.x)*(x - dest.x) + (y - dest.y)*(y - dest.y)));
	}
	
	@Override
	public boolean equals(Object o) {
		Node n = (Node) o;
		return x == n.x && y == n.y;
		//might need a traversed equality
	}

	public int totalCost(){
		return this.cost + heuristic();
	}
	
	@Override
	public int compareTo(Node n) {
		return this.totalCost() - n.totalCost();
	}
	
	@Override
	public int hashCode() {
		return p.hashCode();
	}
	
	public Point getPoint() {
		return new Point(x, y);
	}
	
	public boolean passable() {
		return !type.equals("X");
	}
	
	@Override
	public String toString() {
		return "(" + x + "," + y + ")";
	}
	public boolean isTraversed() {
		return traversed;
	}

	public void setTraversed(boolean traversed) {
		this.traversed = traversed;
	}

}
