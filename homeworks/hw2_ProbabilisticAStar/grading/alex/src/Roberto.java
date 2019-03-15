import java.awt.Point;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashSet;
import java.util.PriorityQueue;

import world.World;

public class Roberto extends BaseRobot {

	private Node[][] grid;
	int currentX;
	int currentY;
	int endX;
	int endY;
	static int worldRows;
	static int worldCols;
	static int radius;
	static int pings;

	public Roberto(Point s, Point f, int c, int r) {
		this.rows = r;
		this.cols = c;
		grid = new Node[r][c];

		for (int i = 0; i < grid.length; i++) {
			for (int j = 0; j < grid[0].length; j++) {

				grid[i][j] = new Node(i, j);
			}
		}
		this.start = new Node(s.x, s.y, "S");
		this.dest = new Node(f.x, f.y, "F");
		grid[s.x][s.y] = new Node(s.x, s.y, "S");
		grid[f.x][f.y] = new Node(f.x, f.y, "F");
	}

	public Roberto() {

	}

	public ArrayList<Node> astar(Node start, Node dest) {
		PriorityQueue<Node> open = new PriorityQueue<Node>();
		HashSet<Node> closed = new HashSet<Node>();

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
				open.add(n);
				n.parent = current;
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
		boolean bot = n.x != (rows - 1);
		boolean left = n.y != 0;
		boolean right = n.y != (cols - 1);

		if (top)
			if (grid[n.x - 1][n.y].passable())
				neighbors.add(grid[n.x - 1][n.y]);
		if (left)
			if (grid[n.x][n.y - 1].passable())
				neighbors.add(grid[n.x][n.y - 1]);
		if (top && left)
			if (grid[n.x - 1][n.y - 1].passable())
				neighbors.add(grid[n.x - 1][n.y - 1]);
		if (bot) {
			if (grid[n.x + 1][n.y].passable()) {
				neighbors.add(grid[n.x + 1][n.y]);
			}
		}
		if (bot && left)
			if (grid[n.x + 1][n.y - 1].passable())
				neighbors.add(grid[n.x + 1][n.y - 1]);
		if (right)
			if (grid[n.x][n.y + 1].passable())
				neighbors.add(grid[n.x][n.y + 1]);
		if (top && right)
			if (grid[n.x - 1][n.y + 1].passable())
				neighbors.add(grid[n.x - 1][n.y + 1]);
		if (bot && right)
			if (grid[n.x + 1][n.y + 1].passable())
				neighbors.add(grid[n.x + 1][n.y + 1]);

		return neighbors;
	}

	private void induceParanoia() {
		// clear the map of any non-traversed walls
		for (int i=0; i<rows; i++)
			for (int j=0; j<cols; j++)
				if (!grid[i][j].passable() && !grid[i][j].isTraversed())
					grid[i][j].type = "O";
	}
	
	public void travelToDestination() {
		// assuming the map is built with all O's and marked S and F Nodes
		// replace the following line with the ping function to initialize
		// the area around you
		ping();

		Node curr = start;
		do {
			Node old = curr;
			ArrayList<Node> path;
			try {
				path = astar(curr, dest);
			} catch (Exception e) {
				// robot thinks there are no valid paths
				// the robot believes the world to be a lie!
				induceParanoia();
				// there has to be a path now!
				path = astar(curr, dest);
			}
			Point newPoint;
			for (Node n : path) {
				newPoint = super.move(n.p);
				if (newPoint.equals(old.p)) {
					// hit a wall, path is now invalid
					// update mental map here => Node n is a traversed wall
					updateMentalMapMove(n.p.x, n.p.y);

					// ping the area around you - possibly skip Nodes
					// that you have already traversed in order to save a few pings
					ping();

					// time to recompute astar since robot's new location !=
					// dest
					// exit from path
					break;
				}
				// path still good!
				else {
					old = grid[newPoint.x][newPoint.y];
				}
			}
			curr = old;

		} while (!dest.equals(curr));

	}

	public void updateMentalMapMove(int x, int y) {
		String temp = super.pingMap(new Point(x, y));
		this.setCurrentPos(this.getPosition());
		if (0 <= x && x < worldRows && 0 <= y && y < worldCols) {
			if (x == currentX && y == currentY) {
				if (grid[x][y].isTraversed() == false) {
					grid[x][y].setTraversed(true);
					grid[x][y].type = temp;
				}

			} else if (x == endX && y == endY) {
				grid[x][y].type = "F";
			} else if ((x >= (currentX - 1)) && (x <= (currentX + 1))
					&& (y >= (currentY - 1)) && (y <= (currentY + 1))) {

				grid[x][y].setTraversed(true);
				grid[x][y].type = "X";
			}
		}
	}

	public void updateMentalMapPing(String value, int x, int y) {

		if (grid[x][y].isTraversed() == false) {
			if (0 <= x && x < worldRows && 0 <= y && y < worldCols) {
				grid[x][y].type = value;
				if (x == currentX && y == currentY) {
					grid[x][y].setTraversed(true);
				}
			}
		}
	}

	public void ping() {
		int pingAmount = pings;

		String temp = "";

		this.setCurrentPos(this.getPosition());
		for (int k = currentX - radius; k <= currentX + radius; k++) {
			for (int l = currentY - radius; l <= currentY + radius; l++) {

				if (0 <= k && k < worldRows && 0 <= l && l < worldCols) {
					if (k == currentX && l == currentY) {
						String here = super.pingMap(new Point(k, l));
						updateMentalMapPing(here, k, l);
					}

					else {
						if (!grid[k][l].isTraversed()) {
							int numberX = 0;
							int numberO = 0;
							for (int i = 0; i < pingAmount; i++) {
								temp = super.pingMap(new Point(k, l));

								if (temp.equals("O")) {
									numberO++;
								} else if (temp.equals("X")) {
									numberX++;
								}
							}
							if (numberO > numberX) {
								updateMentalMapPing("O", k, l);
							} else if (numberO < numberX) {
								updateMentalMapPing("X", k, l);
							} else {
								updateMentalMapPing(temp, k, l);
							}
							temp = "";
						}
					}
				}
			}
		}

	}

	public static void main(String args[]) {
		try {
			World myWorld = new World("input10.txt", true);
			worldRows = myWorld.numRows();
			worldCols = myWorld.numCols();

			radius = 5;
			pings = 1;
			Roberto myRobot = new Roberto(myWorld.getStartPos(),
					myWorld.getEndPos(), worldCols, worldRows);
			myRobot.addToWorld(myWorld);

			myRobot.travelToDestination();

		} catch (Exception e) {
			e.printStackTrace();
		}
	}

	public void printGrid() {
		System.out.println("printGrid()");
		for (int i = 0; i < grid.length; i++) {
			for (int j = 0; j < grid[0].length; j++) {
				System.out.print(grid[i][j].type + " ");
			}
			System.out.println();
		}
		System.out.println();
	}

	public void printTraversedGrid() {
		System.out.println("printTraversedGrid()");
		for (int i = 0; i < grid.length; i++) {
			for (int j = 0; j < grid[0].length; j++) {
				System.out.print(grid[i][j].isTraversed() + " ");
			}
			System.out.println();
		}
		System.out.println();
	}
	
	public void setCurrentPos(Point p) {

		currentX = p.x;
		currentY = p.y;
	}
}
