import java.awt.Point;
import java.util.ArrayList;
import java.util.HashMap;

import world.Robot;

public class NoteTakingRobot extends UncertainRobot {

	private double[][] fscore;
	private double[][] gscore;
	private double[][] probabilities;
	private double wh, wg;
	private ArrayList<Point> closed = new ArrayList<Point>();
	private ArrayList<Point> open = new ArrayList<Point>();
	private ArrayList<Point> neighbors;
	private HashMap<Point, Point> cameFrom = new HashMap<Point, Point>();

	private Point start;
	private Point end;
	private int numCols, numRows;
	private double threshold;

	public NoteTakingRobot(Point start, Point end, int numRows, int numCols, double threshold) {
		super();
		this.start = start;
		this.end = end;
		this.numCols = numCols;
		this.numRows = numRows;
		fscore = new double[numRows][numCols];
		gscore = new double[numRows][numCols];
		probabilities = new double[numRows][numCols];
		this.threshold = threshold;
		for (int x = 0; x < numRows; x++) {
			for (int y = 0; y < numCols; y++) {
				fscore[x][y] = fscore.length * fscore[0].length;
				gscore[x][y] = 0;
				probabilities[x][y] = -1;
			}
		}

	}
	
	public NoteTakingRobot(Point start, Point end, int numRows, int numCols) {
		this(start, end, numRows, numCols, .5);
	}

	public void travelToDestination(int depth) {
		open.add(getPosition());
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
				cameFrom(end);
				continue;
			} else if(cameFrom.size() == depth) {
				cameFrom(current);
				continue;
			}

			open.remove(current);
			closed.add(current);
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

	private void cameFrom(Point expectedEnd) {
		ArrayList<Point> reversedPath = new ArrayList<Point>();
		Point curr = expectedEnd;
		while (!curr.equals(start)) {
			reversedPath.add(curr);
			curr = cameFrom.get(curr);
		}
		reversedPath.add(start);
		for (int i = reversedPath.size() - 1; i >= 0; i--) {
			Point before = this.getPosition();
			this.move(reversedPath.get(i));
			Point after = this.getPosition();
			if(before.equals(after)) {
				probabilities[(int) reversedPath.get(i).getX()][(int) reversedPath.get(i).getY()] = 0;
			} else {
				probabilities[(int) reversedPath.get(i).getX()][(int) reversedPath.get(i).getY()] = 1;
			}
			System.out.println(reversedPath.get(i));
		}
		// reset start to wherever robot ends up
		this.start = this.getPosition();
		// clear cameFrom
		cameFrom.clear();
		// reset closed/open
		closed.clear();
		open.clear();
		open.add(getPosition());
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
			if (sy > 0 && (probabilities[sx+1][sy-1] >= threshold || !this.pingMap(new Point(sx + 1, sy - 1)).equals("X"))) {
				neighbors.add(new Point(sx + 1, sy - 1));
				if(probabilities[sx+1][sy-1] != 0 && probabilities[sx+1][sy-1] != 1) {
					probabilities[sx+1][sy-1] = 1.0 / heuristic(this.getPosition(), neighbors.get(neighbors.size() - 1));
				}
				// probabilitiy = 1/distance
			} else if (sy > 0 && this.pingMap(new Point(sx + 1, sy - 1)).equals("X")) {
				// probability = 1- 1/distance
				if(probabilities[sx+1][sy-1] != 0 && probabilities[sx+1][sy-1] != 1) {
					probabilities[sx+1][sy-1] = 1 - (1.0 / heuristic(this.getPosition(), new Point(sx+1, sy-1)));
				}
			}
			
			if (probabilities[sx+1][sy] >= threshold || !this.pingMap(new Point(sx + 1, sy)).equals("X")) {
				neighbors.add(new Point(sx + 1, sy));
				if(probabilities[sx+1][sy] != 0 && probabilities[sx+1][sy] != 1) {
					probabilities[sx+1][sy] = 1.0 / heuristic(this.getPosition(), neighbors.get(neighbors.size() - 1));
				}
			} else if (this.pingMap(new Point(sx + 1, sy)).equals("X")) {
				// probability = 1- 1/distance
				if(probabilities[sx+1][sy] != 0 && probabilities[sx+1][sy] != 1) {
					probabilities[sx+1][sy] = 1 - (1.0 / heuristic(this.getPosition(), new Point(sx+1, sy)));
				}
			}
			
			if (sy < numCols - 1
					&& (probabilities[sx+1][sy+1] >= threshold || !this.pingMap(new Point(sx + 1, sy + 1)).equals("X"))) {
				neighbors.add(new Point(sx + 1, sy + 1));
				if(probabilities[sx+1][sy+1] != 0 && probabilities[sx+1][sy+1] != 1) {
					probabilities[sx+1][sy+1] = 1.0 / heuristic(this.getPosition(), neighbors.get(neighbors.size() - 1));
				}
			} else if (sy < numCols - 1 && this.pingMap(new Point(sx + 1, sy + 1)).equals("X")) {
				// probability = 1- 1/distance
				if(probabilities[sx+1][sy+1] != 0 && probabilities[sx+1][sy+1] != 1) {
					probabilities[sx+1][sy+1] = 1 - (1.0 / heuristic(this.getPosition(), new Point(sx+1, sy+1)));
				}
			}
		}

		if (sx > 0) {
			if (sy > 0 && (probabilities[sx-1][sy-1] >= threshold || !this.pingMap(new Point(sx - 1, sy - 1)).equals("X"))) {
				neighbors.add(new Point(sx - 1, sy - 1));
				if(probabilities[sx-1][sy-1] != 0 && probabilities[sx-1][sy-1] != 1) {
				probabilities[sx-1][sy-1] = 1.0 / heuristic(this.getPosition(), neighbors.get(neighbors.size() - 1));
				}
			} else if (sy > 0 && this.pingMap(new Point(sx - 1, sy - 1)).equals("X")) {
				// probability = 1- 1/distance
				if(probabilities[sx-1][sy-1] != 0 && probabilities[sx-1][sy-1] != 1) {
					probabilities[sx-1][sy-1] = 1 - (1.0 / heuristic(this.getPosition(), new Point(sx-1, sy-1)));
				}
			}
			
			if ((probabilities[sx-1][sy] >= threshold || !this.pingMap(new Point(sx - 1, sy)).equals("X"))) {
				neighbors.add(new Point(sx - 1, sy));
				if(probabilities[sx-1][sy] != 0 && probabilities[sx-1][sy] != 1) {
					probabilities[sx-1][sy] = 1.0 / heuristic(this.getPosition(), neighbors.get(neighbors.size() - 1));
				}
			} else if (this.pingMap(new Point(sx - 1, sy)).equals("X")) {
				// probability = 1- 1/distance
				if(probabilities[sx-1][sy] != 0 && probabilities[sx-1][sy] != 1) {
					probabilities[sx-1][sy] = 1 - (1.0 / heuristic(this.getPosition(), new Point(sx-1, sy)));
				}
			}
			
			if (sy < numCols - 1
					&& (probabilities[sx-1][sy+1] >= threshold || !this.pingMap(new Point(sx - 1, sy + 1)).equals("X"))) {
				neighbors.add(new Point(sx - 1, sy + 1));
				if(probabilities[sx-1][sy+1] != 0 && probabilities[sx-1][sy+1] != 1) {
					probabilities[sx-1][sy+1] = 1.0 / heuristic(this.getPosition(), neighbors.get(neighbors.size() - 1));
				}
			} else if (sy < numCols - 1 && this.pingMap(new Point(sx - 1, sy + 1)).equals("X")) {
				// probability = 1- 1/distance
				if(probabilities[sx-1][sy+1] != 0 && probabilities[sx-1][sy+1] != 1) {
					probabilities[sx-1][sy+1] = 1 - (1.0 / heuristic(this.getPosition(), new Point(sx-1, sy+1)));
				}
			}
		}

		if (sy > 0 && (probabilities[sx][sy-1] >= threshold || !this.pingMap(new Point(sx, sy - 1)).equals("X"))) {
			neighbors.add(new Point(sx, sy - 1));
			if(probabilities[sx][sy-1] != 0 && probabilities[sx][sy-1] != 1) {
				probabilities[sx][sy-1] = 1.0 / heuristic(this.getPosition(), neighbors.get(neighbors.size() - 1));
			}
		} else if (sy > 0 && this.pingMap(new Point(sx, sy - 1)).equals("X")) {
			// probability = 1- 1/distance
			if(probabilities[sx][sy-1] != 0 && probabilities[sx][sy-1] != 1) {
				probabilities[sx][sy-1] = 1 - (1.0 / heuristic(this.getPosition(), new Point(sx, sy-1)));
			}
		}
		
		if (sy < numCols - 1
				&& (probabilities[sx][sy+1] >= threshold || !this.pingMap(new Point(sx, sy + 1)).equals("X"))) {
			neighbors.add(new Point(sx, sy + 1));
			if(probabilities[sx][sy+1] != 0 && probabilities[sx][sy+1] != 1) {
				probabilities[sx][sy+1] = 1.0 / heuristic(this.getPosition(), neighbors.get(neighbors.size() - 1));
			}
		} else if (sy < numCols - 1 && this.pingMap(new Point(sx, sy + 1)).equals("X")) {
			// probability = 1- 1/distance
			if(probabilities[sx][sy+1] != 0 && probabilities[sx][sy+1] != 1) {
				probabilities[sx][sy+1] = 1 - (1.0 / heuristic(this.getPosition(), new Point(sx, sy+1)));
			}
		}
		return spot;
	}

	private static double heuristic(int sx, int sy, int ex, int ey) {
		// number of steps to get from s to end
		return Math.sqrt(Math.pow(sx - ex, 2) + Math.pow(sy - ey, 2));
	}
	
	private static double heuristic(Point start, Point end) {
		// number of steps to get from s to end
		return Math.sqrt(Math.pow(start.getX() - end.getX(), 2) + Math.pow(start.getY() - end.getY(), 2));
	}

	@Override
	public void travelToDestination() {
		this.travelToDestination(1);
	}
}
