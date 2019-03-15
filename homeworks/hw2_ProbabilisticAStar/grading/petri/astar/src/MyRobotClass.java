import java.awt.Point;
import java.util.ArrayList;
import java.util.Collections;

import world.Robot;
import world.World;


public class MyRobotClass extends Robot{
	public MyPoint start;
	public MyPoint finish;
	public int xDimension;
	public int yDimension;
	public boolean uncertainty;
	
	public MyRobotClass(MyPoint s, MyPoint f, int x, int y, boolean u) {
		start = s;
		finish = f;
		xDimension = x;
		yDimension = y;
		uncertainty = u;
	}
	
	public double heuristic(MyPoint start, MyPoint finish) {
		int sX = start.x;
		int sY = start.y;
		int fX = finish.x;
		int fY = finish.y;
		int diffX = Math.abs(start.x-finish.x);
		int diffY = Math.abs(start.y-finish.y);
		if (diffX > diffY){
			return (14*diffY) + (10*(diffX-diffY));
		}
		else{
			return (14*diffX) + (10*(diffY-diffX));
		}

		

//		return Math.sqrt(Math.pow((fX - sX),2) + Math.pow((fY - sY),2));
	}
	
	public ArrayList<MyPoint> getNeighbors(MyPoint current) {
		ArrayList<MyPoint> neighbors = new ArrayList<MyPoint>();
		int currX = current.x;
		int currY = current.y;
		int xdim = this.xDimension;
		int ydim = this.yDimension;
		int newCurrX;
		int newCurrY;
		for (int i = -1; i < 2; i++){
            for (int j = -1; j <2; j++){
            	newCurrX = currX+i;
            	newCurrY = currY+j;
            	if (newCurrX >= 0 && newCurrY >= 0 && newCurrX < xdim && newCurrY < ydim){
            		MyPoint p = new MyPoint(newCurrX,newCurrY,current);
            		neighbors.add(p);
            	}         
            }
		}
		return neighbors;
	}
	
	public double getGScore(MyPoint current) {
		return current.parent.path + 1;
	}
	
	public double getFScore(MyPoint current) {
		return this.getGScore(current) + this.heuristic(current, finish);
	}

	
	public void pathfinder_uncertain(MyPoint last) {
		ArrayList<MyPoint> points = new ArrayList<MyPoint>();
		
		points.add(last);
		last = last.parent;		
		while (last.x != start.x && last.y != start.y){
			points.add(last);
			last = last.parent;
		}
		points.add(last);
		Collections.reverse(points);
		
		for (MyPoint p : points){
			Point po = new Point(p.x,p.y);
			Point s = new Point(start.x,start.y);
			if (!po.equals(s)){
			System.out.println("Moving to: " + po);
			super.move(po);
			}
			if (!po.equals(this.getPosition())){
				this.travelToDestination();
			}

		}
		return;
	}
	public void pathfinder_certain(MyPoint last) {
		ArrayList<MyPoint> points = new ArrayList<MyPoint>();
		
		points.add(last);
		last = last.parent;		
		while (last.x != start.x && last.y != start.y){
			points.add(last);
			last = last.parent;
		}
		points.add(last);
		Collections.reverse(points);
		for (int q = 0; q <points.size(); q++){
			System.out.println("Point "+q+": "+points.get(q).x+","+points.get(q).y);
		}
		
		for (MyPoint p : points){
			Point po = new Point(p.x,p.y);
			Point s = new Point(start.x,start.y);
			if (!po.equals(s)){
				System.out.println("Moving to: " + po);
				super.move(po);
			}
			if (!po.equals(this.getPosition())){
				System.out.println("The robot didnt move to "+ po.x + ","+po.y);
			}
			else{
				System.out.println("one");
			}
			

		}
	}
	
	@Override
	public void travelToDestination() {
		if(this.uncertainty == false) {
			ArrayList<MyPoint> closed = new ArrayList<MyPoint>();
			ArrayList<MyPoint> open = new ArrayList<MyPoint>();
			
			open.add(start);
			start.path = 0;
			start.parent = new MyPoint(-1,-1);
	
			while(!open.isEmpty()) {
				MyPoint current = new MyPoint(0,0);
				double min = 100000000;
				for (MyPoint p : open){
					if (p.fscore < min){
						min = p.fscore;
						current = p;
					}
				}
				
				open.remove(current);
				closed.add(current);
			
				if(current.equals(finish)) {
					System.out.println("You reached the finish node!");
					this.pathfinder_certain(current);
					return;
				}
				
				ArrayList<MyPoint> possibleSpots = new ArrayList<MyPoint>();
				for(MyPoint neighbor : this.getNeighbors(current)) {
					if(closed.contains(neighbor)) {
						continue;
					}				
					
					Point p = new Point (neighbor.x,neighbor.y);
					String spot = super.pingMap(p);
					if(spot.equals("O") || spot.equals("F")) {
						possibleSpots.add(neighbor);
					}
				}
				
				ArrayList<Double> neighborScores = new ArrayList<Double>();
				for(MyPoint neighbor : possibleSpots) {	
					double tempGScore = this.getGScore(current) + this.heuristic(neighbor, finish);
					neighborScores.add(tempGScore);
					if(!open.contains(neighbor)) {
						neighbor.parent = current;
						neighbor.gscore = this.getGScore(neighbor);
						neighbor.fscore = this.getFScore(neighbor);
						neighbor.hscore = this.heuristic(neighbor, finish);
						open.add(neighbor);
					} else {
						if(neighbor.gscore < current.gscore) {
							neighbor.parent = current;
							neighbor.gscore = this.getGScore(current);
							neighbor.fscore = this.getFScore(neighbor);
							open.add(neighbor);
						}
					}
					
				}
			}
		}
		
		//^certain Vuncertain
		
		else {
			ArrayList<MyPoint> closed = new ArrayList<MyPoint>();
			ArrayList<MyPoint> open = new ArrayList<MyPoint>();
			
			open.add(start);
			start.path = 0;
			start.parent = new MyPoint(-1,-1);
	
			while(!open.isEmpty()) {
				MyPoint current = new MyPoint(0,0);
				double min = 100000000;
				for (MyPoint p : open){
					if (p.fscore < min){
						min = p.fscore;
						current = p;
					}
				}
				
				open.remove(current);
				closed.add(current);
			
				if(current.equals(finish)) {
					System.out.println("You reached the finish node!");
					this.pathfinder_uncertain(current);
					return;
				}
				
				ArrayList<MyPoint> possibleSpots = new ArrayList<MyPoint>();
				for(MyPoint neighbor : this.getNeighbors(current)) {
					if(closed.contains(neighbor)) {
						continue;
					}				
					
					Point p = new Point (neighbor.x,neighbor.y);
					String spot = super.pingMap(p);
					if(spot.equals("O") || spot.equals("F")) {
						possibleSpots.add(neighbor);
					}
				}
				
				ArrayList<Double> neighborScores = new ArrayList<Double>();
				for(MyPoint neighbor : possibleSpots) {	
					double tempGScore = this.getGScore(current) + this.heuristic(neighbor, finish);
					neighborScores.add(tempGScore);
					if(!open.contains(neighbor)) {
						neighbor.parent = current;
						neighbor.gscore = this.getGScore(neighbor);
						neighbor.fscore = this.getFScore(neighbor);
						neighbor.hscore = this.heuristic(neighbor, finish);
						open.add(neighbor);
					} else {
						if(neighbor.gscore < current.gscore) {
							neighbor.parent = current;
							neighbor.gscore = this.getGScore(current);
							neighbor.fscore = this.getFScore(neighbor);
							open.add(neighbor);
						}
					}
					
				}
			}
		}
	}
	
	public static void main(String [] args) {
		try {
			Boolean u = false;
			World world = new World(args[0],u );
			MyPoint s = new MyPoint(world.getStartPos());
			MyPoint f = new MyPoint(world.getEndPos());
			System.out.println("Start: " + s);
			System.out.println("Finish: " + f);
			MyRobotClass r = new MyRobotClass(s, f, world.numRows(), world.numCols(),u);
			r.addToWorld(world);
			r.travelToDestination();
			System.out.println(r.getNumMoves());
			System.out.println(r.getNumPings());
		} catch(Exception e) {
			e.printStackTrace();
		}
	}
}
