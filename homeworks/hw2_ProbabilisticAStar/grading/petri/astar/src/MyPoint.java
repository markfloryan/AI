import java.awt.Point;

public class MyPoint extends Point {
	public Point point;
	public int x;
	public int y;
	public MyPoint parent;
	public double fscore;
	public double gscore;
	public double hscore;
	public int path;
	
	public MyPoint(Point p) {
		point = p;
		x = p.x;
		y = p.y;
		parent = null;
	}
	
	public MyPoint(int x0, int y0,MyPoint par) {
		point = new Point(x0,y0);
		x = x0;
		y = y0;
		parent = par;
	}
	
	public MyPoint(int x0, int y0) {
		point = new Point(x0,y0);
		x = x0;
		y = y0;
		parent = null;
	}
	public MyPoint(Point p,MyPoint par) {
		point = p;
		x = p.x;
		y = p.x;
		parent = par;
	}
	

	
	public int getX(Point p) {
		return this.x;
	}
	
	public int getY(Point p) {
		return this.y;
	}

	@Override
	public boolean equals(Object obj){
		MyPoint o = (MyPoint) obj;
		if (this.x != o.x || this.y != o.y){
			return false;
		}
		return true;
	}
}
