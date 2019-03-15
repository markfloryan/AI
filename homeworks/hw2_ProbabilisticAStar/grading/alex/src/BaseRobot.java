
import java.awt.Point;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashSet;
import java.util.PriorityQueue;

import world.Robot;
import world.World;

public class BaseRobot extends Robot {
	// fields
	Node start, dest;
	int rows, cols;
	Node[][] map;
	
	public BaseRobot (Point s, Point f, int w, int h) {
		this.start = new Node(s.x, s.y, "S");
		this.dest = new Node(f.x, f.y, "F");
		this.rows = h;
		this.cols = w;
		map = new Node[rows][cols];
	}
	
	public BaseRobot () { }

	public ArrayList<Node> astar(Node start, Node dest) {
		PriorityQueue<Node> open = new PriorityQueue<Node>();
		HashSet<Node> closed = new HashSet<Node>();
		
		start.cost = 0;
		open.add(start);
		Node current;
		// find path
		do {
			// get node of smallest cost and add it to the closed set
			current = open.remove();
			closed.add(current);
			// for each unvisited neighbor of current
			for (Node n : getNeighbors(current)) {
				int updatedCost = n.cost + 1;

				if (open.contains(n) || closed.contains(n))
					continue;
				n.cost = updatedCost;
				n.parent = current;
				open.add(n);
				
			}
			
		} while (!current.equals(dest));
			
		// reconstruct path
		ArrayList<Node> path = new ArrayList<Node>();
		while (!current.equals(start)) {
			path.add(current);
			current = current.parent;
		}
		Collections.reverse(path);
			
		return path;
	}
		
	private ArrayList<Node> getNeighbors(Node n) {
		ArrayList<Node> neighbors = new ArrayList<Node>();
		
		boolean top = n.x != 0;
		boolean bot = n.x != (rows-1);
		boolean left = n.y != 0;
		boolean right = n.y != (cols-1);
		
		if (top)
			if (map[n.x-1][n.y].passable())
				neighbors.add(map[n.x-1][n.y]);
		if (left)
			if (map[n.x][n.y-1].passable())
				neighbors.add(map[n.x][n.y-1]);
		if (top && left)
			if (map[n.x-1][n.y-1].passable())
				neighbors.add(map[n.x-1][n.y-1]);
		if (bot)
			if (map[n.x+1][n.y].passable())
				neighbors.add(map[n.x+1][n.y]);
		if (bot && left)
			if (map[n.x+1][n.y-1].passable())
				neighbors.add(map[n.x+1][n.y-1]);
		if (right)
			if (map[n.x][n.y+1].passable())
				neighbors.add(map[n.x][n.y+1]);
		if (top && right)
			if (map[n.x-1][n.y+1].passable())
				neighbors.add(map[n.x-1][n.y+1]);
		if (bot && right)
			if (map[n.x+1][n.y+1].passable())
				neighbors.add(map[n.x+1][n.y+1]);
		
		return neighbors;
	}
	
	private void buildMap() {
		// build map
		Node.dest = dest;
		for (int i=0; i<rows; i++)
			for (int j=0; j<cols; j++)
				map[i][j] = new Node(i, j, pingMap(new Point(i, j)));
	}
	
	@Override
	public void travelToDestination() {
		buildMap();
		// run A*
		ArrayList<Node> path = astar(start, dest);
		
		// execute path
		for (Node n : path){
			System.out.println("Moving to: " + n.getPoint());
			move(n.getPoint());
		}
	}
	
	public static void main(String[] args) {
		try {
			World world = new World("input4.txt", false);
			
			BaseRobot omniRobit = new BaseRobot(world.getStartPos(), world.getEndPos(), world.numCols(), world.numRows());
			omniRobit.addToWorld(world);
			
			omniRobit.travelToDestination();
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
}
