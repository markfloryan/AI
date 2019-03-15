import java.awt.Point;

public class Node {
	public Node parent;
	public Point pos;
	public double f, g, h;
	public String ping;
	
	
	
	public Node (Point coord, String val){
	//	parent = p;
	//	left = l;
	//	right = r;
		pos = coord;
		ping = val;
	}
}

