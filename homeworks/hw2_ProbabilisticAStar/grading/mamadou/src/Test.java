import java.awt.Point;

import world.World;


public class Test {

	/**
	 * @param args
	 * @throws Exception File does not exist.
	 */
	public static void main(String[] args) throws Exception {
		// TODO Auto-generated method stub
		boolean uncertainty = false;
		World myWorld = new World(args[0], uncertainty);

		MyRobotClass myRobot = new MyRobotClass();
		myRobot.addToWorld(myWorld);
		myRobot.passInfo(myWorld.getEndPos(), myWorld.numRows(), myWorld.numCols(),uncertainty);
		
		myRobot.travelToDestination();
	//	myRobot.move(new Point(5,4));
	}

}
