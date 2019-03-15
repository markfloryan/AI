import java.awt.Point;
import java.util.ArrayList;

public class NodeList {
	public ArrayList<Node> list;

	public NodeList() {
		list = new ArrayList<Node>();
	}

	public int getLeast() {
		double least = Double.MAX_VALUE;
		int index = 0;

		for (int i = 0; i < this.list.size(); i++) {
			if (this.list.get(i).f < least) {
				index = i;
				least = this.list.get(i).f;
			}
		}
		return index;
	}
	
	public boolean lowerF(Node s){
		boolean result = false;
		for(int i = 0; i < this.list.size();i++){
			if(this.list.get(i).f < s.f){
				result = true;
			}
		}
		return result;
	}
	
	public Node contains(Point p){
		boolean result = false;
		for(int i = 0; i < this.list.size();i++){
			if(this.list.get(i).pos.equals(p)){
				return this.list.get(i);
			}
		}
		return null;
	}
	
	public void replace(Point p, Node n){
		for(int i = 0; i < this.list.size();i++){
			if(this.list.get(i).pos.equals(p)){
				this.list.set(i, n);
				break;
			}
		}
	}

}
