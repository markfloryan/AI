import world.Robot;
import world.World;


public class Driver {
	// name of test case
	// uncertainty
	// type of robot
	// threshold
	// depth
	
	public static void main(String[] args) throws Exception {
		World myWorld = new World(args[0], Boolean.parseBoolean(args[1]));
		UncertainRobot myRobot;
		
		if(args[2].equals("0") && Boolean.parseBoolean(args[1])) {
			Robot myRobot2 = new CertainRobot(myWorld.getStartPos(), myWorld.getEndPos(), myWorld.numRows(), myWorld.numCols());
			myRobot2.travelToDestination();
			return;
		} else if(args[2].equals("1") && !Boolean.parseBoolean(args[1])) {
			myRobot = new IndecisiveRobot(myWorld.getStartPos(), myWorld.getEndPos(), myWorld.numRows(), myWorld.numCols());
		} else if(args.length > 3) {
			myRobot = new NoteTakingRobot(myWorld.getStartPos(), myWorld.getEndPos(), myWorld.numRows(), myWorld.numCols(), Double.parseDouble(args[3]));
		} else {
			myRobot = new NoteTakingRobot(myWorld.getStartPos(), myWorld.getEndPos(), myWorld.numRows(), myWorld.numCols());
		}
		
		myRobot.addToWorld(myWorld);
		
		if(args.length < 4 || args[2].equals("1")) {
		myRobot.travelToDestination();
		} else {
			myRobot.travelToDestination(Integer.parseInt(args[4]));
		}
	}

}
