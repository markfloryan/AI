import world.World;
import world.Robot;

public class Main{

	public static void main(String[] args){

		try{
			World myWorld = new World(args[0], false);

			CertainRobot robot = new CertainRobot(myWorld.getStartPos(), myWorld.getEndPos(), myWorld.numRows(), myWorld.numCols());
			robot.addToWorld(myWorld);

			robot.travelToDestination();
		}
		catch(Exception e){
			e.printStackTrace();
		}
	}


}
