import world.Robot;
import world.World;
import java.util.ArrayList;
import java.awt.Point;
import java.util.PriorityQueue;

public class MyRobot extends Robot{


	private World world;
	private String map[][];


	public void travelToDestination(World myWorld){
		world = myWorld;
		travelToDestination();
	}

	@Override
	public void travelToDestination(){
		System.out.println("Time to travel");

		/* Read in the whole map  */
		map = new String[world.numRows()][world.numCols()];

		for(int i=0; i<world.numRows(); i++){
			for(int j=0; j<world.numCols(); j++){
				map[i][j] = pingMap(new Point(i,j));
				System.out.print(map[i][j] + " ");
			}
			System.out.println();
		}

		ArrayList<Node> path = runAStar();

		for(Node node : path){
			System.out.println(node.position.x + ", " + node.position.y);
			super.move(node.position);
		}
	}



	/* A Star Algorithm. Returns a list of points to travel to  */
	private ArrayList<Node> runAStar(){

		PriorityQueue<Node> queue = new PriorityQueue<Node>(100, new NodeComparator());
		Node start = new Node(world.getStartPos(), 0, h(world.getStartPos()));

		queue.add(start);


		Node finalNode = null;
		while(queue.size() > 0){
			Node next = queue.poll();

			if(isFinalPos(next.position)){
				finalNode = next;
				break;
			}
			/*Generate neighbors*/
			ArrayList<Node> neighbors = generateNeighbors(next);

			for(Node neighbor : neighbors){
				neighbor.previous = next;
				updateQueue(queue, neighbor);
			}
		}

		if(finalNode == null){System.out.println("Something is wrong, final node is null");}


		/*Generate the path*/
		ArrayList<Node> path = new ArrayList<Node>();

		generatePath(finalNode, path);

		return path;
	}

	/* Generates the path starting at the end node */
	private void generatePath(Node node, ArrayList<Node> path){

		if(node.previous != null)
			generatePath(node.previous, path);
		path.add(node);
	}

	/*AStar Heuristic*/
	private double h(Point pos){
		return pos.distance(world.getEndPos());
	}

	private boolean isFinalPos(Point point){
		return (point.x == world.getEndPos().x && point.y == world.getEndPos().y);
	}

	private ArrayList<Node> generateNeighbors(Node node){
		/* just return every possible valid neighbor  */

		ArrayList<Node> neighbors = new ArrayList<Node>();

		for(int xOff=-1; xOff<=1; xOff++){
			for(int yOff=-1; yOff<=1; yOff++){
				if(xOff==0 && yOff==0) continue;

				int newX = node.position.x + xOff;
				int newY = node.position.y + yOff;

				/*if out of bounds, continue*/
				if(newX<0 || newX>=map.length || newY<0 || newY>=map[0].length) continue;

				if(map[newX][newY].equals("X")) continue;

				neighbors.add(new Node(new Point(newX,newY), node.distToNode+1, h(new Point(newX,newY))));
			}
		}

		return neighbors;
	}

	private void updateQueue(PriorityQueue<Node> queue, Node node){
		Object[] array = queue.toArray();
		//System.out.println("in update queue");
		boolean found = false;
		for(int i=0; i<array.length; i++){
			if(node.equals((Node)array[i])){
				//System.out.println("found equal node: " + array[i]);
				found = true;
				if(node.distToNode < ((Node)array[i]).distToNode){
					queue.remove((Node)array[i]);
					queue.add(node);
				}
				return;
			}
		}

		if(!found) queue.add(node);
	}
}
