import java.awt.Point;
import java.util.ArrayList;
import java.util.HashMap;

import world.Robot;

public class CertainRobot extends Robot {

	private double[][] fscore;
	private double[][] gscore;
	private double wh, wg;
	private ArrayList<Point> closed = new ArrayList<Point>();
	private ArrayList<Point> open = new ArrayList<Point>();
	private ArrayList<Point> neighbors;
	private HashMap<Point, Point> cameFrom = new HashMap<Point, Point>();

	private Point start;
	private Point end;
	private int numCols, numRows;

	public CertainRobot(Point start, Point end, int numRows, int numCols) {
		super();
		this.start = start;
		this.end = end;
		this.numCols = numCols;
		this.numRows = numRows;
		fscore = new double[numRows][numCols];
		gscore = new double[numRows][numCols];
		for (int x = 0; x < numRows; x++) {
			for (int y = 0; y < numCols; y++) {
				fscore[x][y] = fscore.length * fscore[0].length;
				gscore[x][y] = 0;
			}
		}

	}

	public void travelToDestination() {
		open.add(getPosition());
		cameFrom.put(getPosition(), new Point(-1, -1));
		int sx = (int) start.getX();
		int sy = (int) start.getY();
		int ex = (int) end.getX();
		int ey = (int) end.getY();
		gscore[sx][sy] = 0;
		fscore[sx][sy] = wg * gscore[sx][sy] + wh * heuristic(sx, sy, ex, ey);

		while (open.size() > 0) {
			Point current = findLowest();
			int cx = (int) current.getX();
			int cy = (int) current.getY();
			if (current.equals(end)) {
				// print length of path
				cameFrom();
			}

			open.remove(current);
			closed.add(current);
			System.out.println("Open List: " + open);
			System.out.println("Cur: " + current + ", neighbors: " + neighbors + "\n");

			for (Point n : neighbors) {
				if (closed.contains(n)) {
					continue;
				}
				// dist between current node and neighbor is always 1
				double tentScore = gscore[cx][cy] + 1;
				int nx = (int) n.getX();
				int ny = (int) n.getY();
				if (!open.contains(n) || tentScore < gscore[nx][ny]) {
					cameFrom.put(n, new Point(cx, cy));
					gscore[nx][ny] = tentScore;
					fscore[nx][ny] = wg * gscore[nx][ny] + wh
							* heuristic(nx, ny, ex, ey);
					if (!open.contains(n)) {
						open.add(n);
					}
				}

			}
		}
	}

	private void cameFrom() { 
		ArrayList<Point> reversedPath = new ArrayList<Point>(); 
		Point curr = end;
		while (!curr.equals(start)) {
			reversedPath.add(curr);
			curr = cameFrom.get(curr);
		}
		reversedPath.add(start);
		for (int i = reversedPath.size() - 1; i >= 0; i--) {
			System.out.println("Moving to: " + reversedPath.get(i));
			this.move(reversedPath.get(i));
		}
	}

	private Point findLowest() { // Finds the point with the lowest fscore
		Point spot = new Point();
		double lowest = fscore.length * fscore[0].length + 1;
		for (int x = 0; x < fscore.length; x++) {
			for (int y = 0; y < fscore[0].length; y++) {
				if (fscore[x][y] < lowest && open.contains(new Point(x, y))) {
					lowest = fscore[x][y];
					spot.setLocation(x, y);

				}
			}
		}
		neighbors = new ArrayList<Point>();
		int sx = (int) spot.getX();
		int sy = (int) spot.getY();
		if (sx < numRows - 1) {
			if (sy > 0 && !this.pingMap(new Point(sx + 1, sy - 1)).equals("X")) {
				neighbors.add(new Point(sx + 1, sy - 1));
			}
			if (!this.pingMap(new Point(sx + 1, sy)).equals("X")) {
				neighbors.add(new Point(sx + 1, sy));
			}
			if (sy < numCols - 1
					&& !this.pingMap(new Point(sx + 1, sy + 1)).equals("X")) {
				neighbors.add(new Point(sx + 1, sy + 1));
			}
		}

		if (sx > 0) {
			if (sy > 0 && !this.pingMap(new Point(sx - 1, sy - 1)).equals("X")) {
				neighbors.add(new Point(sx - 1, sy - 1));
			}
			if (!this.pingMap(new Point(sx - 1, sy)).equals("X")) {
				neighbors.add(new Point(sx - 1, sy));
			}
			if (sy < numCols - 1
					&& !this.pingMap(new Point(sx - 1, sy + 1)).equals("X")) {
				neighbors.add(new Point(sx - 1, sy + 1));
			}
		}

		if (sy > 0 && !this.pingMap(new Point(sx, sy - 1)).equals("X")) {
			neighbors.add(new Point(sx, sy - 1));
		}
		if (sy < numCols - 1
				&& !this.pingMap(new Point(sx, sy + 1)).equals("X")) {
			neighbors.add(new Point(sx, sy + 1));
		}
		return spot;
	}

	private static double heuristic(int sx, int sy, int ex, int ey) {
		// number of steps to get from s to end
		return Math.sqrt(Math.pow(sx - ex, 2) + Math.pow(sy - ey, 2));
	}
}
