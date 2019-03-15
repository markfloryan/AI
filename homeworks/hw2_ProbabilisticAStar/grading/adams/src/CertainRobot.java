import java.awt.Point;

import world.Robot;

import java.util.PriorityQueue;
import java.util.HashSet;
import java.util.Set;
import java.util.List;
import java.util.Comparator;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.math.*;

public class CertainRobot extends Robot {
	
	Point startPos;
	Point endPos;
	int rows;
	int columns;
	char[][] matrix;
	
	public CertainRobot(Point inputStartPos, Point inputEndPos, int inputRows, int inputColumns) {
		// doing this because Robot doesn't have access to World methods, so passing in important info from World class to the Robot class
		// piazza question #56 talks about this
		startPos = inputStartPos;
		endPos = inputEndPos;
		rows = inputRows;
		columns = inputColumns;
		matrix = new char[inputRows][inputColumns];
	}

	 HashMap distMap = new HashMap<Point, Integer>(); // map that keeps track of distance for each Point. Not sure why i had to put it here for Comparator to work
	 HashMap fMap = new HashMap<Point, Integer>(); // map that keeps track of the heuristic from that point to end
	 HashMap cameFromMap = new HashMap<Point, Point>(); // map that stores which Point led to the current Point in the path
	 
	 
	public ArrayList<Point> neighbhorPoints(Point p) //finds all Points that aren't an X and are in bounds
	{
		ArrayList<Point> answerList = new ArrayList<Point>();
		
		if (p.x > 0) {
			// If it's already in the matrix
			if (matrix[p.x-1][p.y] == 'O' || matrix[p.x-1][p.y] == 'X') {
				if (matrix[p.x-1][p.y] == 'O') {
					answerList.add(new Point(p.x-1, p.y));
				} 
			} else {
				if(!super.pingMap(new Point(p.x-1,p.y)).equals("X")) {
					answerList.add(new Point(p.x-1,p.y));
					matrix[p.x-1][p.y] = 'O';
				} else {
					matrix[p.x-1][p.y] = 'X';
				}
			}
		}
		
		if (p.x < rows -1) {
			if (matrix[p.x+1][p.y] == 'O' || matrix[p.x+1][p.y] == 'X') {
				if (matrix[p.x+1][p.y] == 'O') {
					answerList.add(new Point(p.x+1, p.y));
				} 
			} else {
				if (!super.pingMap(new Point(p.x+1,p.y)).equals("X")) {
					answerList.add(new Point(p.x+1,p.y));
					matrix[p.x+1][p.y] = 'O';
				} else {
					matrix[p.x+1][p.y] = 'X';
				}
			}
		}
		
		if (p.y > 0) {
			if (matrix[p.x][p.y-1] == 'O' || matrix[p.x][p.y-1] == 'X') {
				if (matrix[p.x][p.y-1] == 'O') {
					answerList.add(new Point(p.x, p.y-1));
				} 
			} else {
				if (!super.pingMap(new Point(p.x,p.y-1)).equals("X")) {
					answerList.add(new Point(p.x,p.y-1));
					matrix[p.x][p.y-1] = 'O';
				} else {
					matrix[p.x][p.y-1] = 'X';
				}
			}
		}
		
		if (p.y < columns -1) {
			if (matrix[p.x][p.y+1] == 'O' || matrix[p.x][p.y+1] == 'X') {
				if (matrix[p.x][p.y+1] == 'O') {
					answerList.add(new Point(p.x, p.y+1));
				} 
			} else {
				if(!super.pingMap(new Point(p.x,p.y+1)).equals("X")) {
					answerList.add(new Point(p.x,p.y+1));
					matrix[p.x][p.y+1] = 'O';
				} else {
					matrix[p.x][p.y+1] = 'X';
				}
			}
		}
		
		if (p.x > 0 && p.y > 0) {
			if (matrix[p.x-1][p.y-1] == 'O' || matrix[p.x-1][p.y-1] == 'X') {
				if (matrix[p.x-1][p.y-1] == 'O') {
					answerList.add(new Point(p.x-1, p.y-1));
				} 
			} else {
				if (!super.pingMap(new Point(p.x-1,p.y-1)).equals("X")) {
					answerList.add(new Point(p.x-1,p.y-1));
					matrix[p.x-1][p.y-1] = 'O';
				} else {
					matrix[p.x-1][p.y-1] = 'X';
				}
			}
		}
		
		if (p.x > 0 && p.y < columns - 1) {
			if (matrix[p.x-1][p.y+1] == 'O' || matrix[p.x-1][p.y+1] == 'X') {
				if (matrix[p.x-1][p.y+1] == 'O') {
					answerList.add(new Point(p.x-1, p.y+1));
				} 
			} else {
				if (!super.pingMap(new Point(p.x-1,p.y+1)).equals("X")) {
					answerList.add(new Point(p.x-1,p.y+1));
					matrix[p.x-1][p.y+1] = 'O';
				} else {
					matrix[p.x-1][p.y+1] = 'X';
				}
			}
		}
		
		if (p.x < rows - 1 && p.y > 0) {
			if (matrix[p.x+1][p.y-1] == 'O' || matrix[p.x+1][p.y-1] == 'X') {
				if (matrix[p.x+1][p.y-1] == 'O') {
					answerList.add(new Point(p.x+1, p.y-1));
				} 
			} else {
				if (!super.pingMap(new Point(p.x+1,p.y-1)).equals("X")) {
					answerList.add(new Point(p.x+1,p.y-1));
					matrix[p.x+1][p.y-1] = 'O';
				} else {
					matrix[p.x+1][p.y-1] = 'X';
				}
			}
		}
		
		if (p.x < rows - 1 && p.y < columns - 1) {
			if (matrix[p.x+1][p.y+1] == 'O' || matrix[p.x+1][p.y+1] == 'X') {
				if (matrix[p.x+1][p.y+1] == 'O') {
					answerList.add(new Point(p.x+1, p.y+1));
				} 
			} else {
				if (!super.pingMap(new Point(p.x+1,p.y+1)).equals("X")) {
					answerList.add(new Point(p.x+1,p.y+1));
					matrix[p.x+1][p.y+1] = 'O';
				} else {
					matrix[p.x+1][p.y+1] = 'X';
				}
			}
		}
		
		return answerList;	
	}
	
	public int dist(Point p1, Point p2) {
		return Math.abs(p1.x - p2.x) + Math.abs(p1.y - p2.y); // heuristic is just Manhattan distance
	}
	
	public void reconstructPath (Point currentPoint) { // called at the end to find the solutionPath and make moves 
		ArrayList<Point> solutionPath = new ArrayList<Point>();// solution path - will need to flip it
		Point p = currentPoint;
		//System.out.println("Solution Path:");
		
		while (!p.equals(startPos)) {
			solutionPath.add(p);
			p = (Point) cameFromMap.get(p);
		}
		
		Collections.reverse(solutionPath); //because we backward chained, need to flip the list to get start -> end path
		
		//System.out.println(solutionPath.size());
		for (Point movePoint: solutionPath) {
			super.move(movePoint); // UNCOMMENT THIS TO ACTUALLY MOVE IT. TURNS DEBUG STATEMENTS OFF THO
		}	
		
	}
	 
	@Override
	public void travelToDestination() {
		 Set<Point> explored = new HashSet<Point>(); // set of Point's already explored
		 PriorityQueue<Point> queue = new PriorityQueue<Point>(rows*columns, new Comparator<Point>(){  // stores points in Priority Queue               
			 public int compare(Point i, Point j) { // TO FIX: Compare's priorities to endPos to see which is closer
				 int iValue = (int) distMap.get(i);
				 int jValue = (int) distMap.get(j);
             
				 if ( iValue >  jValue) {
					 return 1;    
				 } else if (iValue < jValue) {
					 return -1;
				 } else {
					 return 0;
				 }
			 }
		 });
				 
		 boolean found = false;
		 distMap.put(startPos, 0); // starting Node as distance of 0
		 queue.add(startPos);
		 
		 // add in the first point to start the queue
		 while ((!queue.isEmpty()) && (!found)) {
			 Point currentPoint = queue.poll();
			 //System.out.println("Currently examining in the queue point" + currentPoint.x + "," + currentPoint.y);
			 explored.add(currentPoint);
			 
			 if (currentPoint.equals(endPos)) {
				 // Never getting to this point now
				 found = true; // reconstruct path at this point
				 reconstructPath(currentPoint);
				 
			 }
			 
			 for (Point p : neighbhorPoints(currentPoint)) {
				 if (explored.contains(p))
					 continue;
					 
				 int tentative_score = (int) distMap.get(currentPoint) + 1; 
				 
				 if (!queue.contains(p) || tentative_score < (int) distMap.get(p)) { 
					cameFromMap.put(p, currentPoint); 
					distMap.put(p, tentative_score);
					fMap.put(p, (int) distMap.get(p) + dist(p, endPos));
					if (!queue.contains(p)) {
						queue.add(p);
					}
				 }
			 }
		 }
		 

	}
}

class PointComparator implements Comparator<Point> {
	
	@Override
    public int compare(Point p1, Point p2) {
    	
        int dist1 = p1.x - p1.x; // Find Manhattan distance between p1 and end point
        int dist2 = p2.x - p2.y; // Find Manhattan distance between p2 and end point
        if (dist1 > dist2)
        {
        	return 1;
        }
        else if (dist1 < dist2 ){
        	return -1;
        }
        else
        {
        	return 0;
        }
        

    }

}



