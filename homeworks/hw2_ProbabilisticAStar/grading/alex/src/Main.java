import world.World;
import world.Robot;

public class Main{

	public static void main(String[] args){

		try{
			World myWorld = new World(args[0], false);

			BaseRobot robot = new BaseRobot(myWorld.getStartPos(), myWorld.getEndPos(), myWorld.numCols(), myWorld.numRows());
			robot.addToWorld(myWorld);

			robot.travelToDestination();
		}
		catch(Exception e){
			e.printStackTrace();
		}
	}


}
