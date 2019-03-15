import world.World;
import world.Robot;

public class Main{

	public static void main(String[] args){

		try{
			World myWorld = new World("../input/input1", true);

			MyRobot robot = new MyRobot();
			robot.addToWorld(myWorld);

			robot.travelToDestination(myWorld);
		}
		catch(Exception e){
			e.printStackTrace();
		}
	}


}
