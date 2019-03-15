package world;
import java.awt.Point;
import java.io.File;
import java.util.ArrayList;
import java.util.Scanner;
import java.util.StringTokenizer;

/**
 * The world within which our "robots" can interact and move. The world is represented by a two-dimensional array
 * of O and X characters. X means that space is a wall, O means that space is floor (robot can move there). There are
 * two special characters in the world (S and F) which are the start and finish positions respectively.
 * */
public class World {

	/* The world space */
	private ArrayList<ArrayList<String>> worldMap;
	
	/* The location of the special start and finish nodes */
	private Point startPos;
	private Point endPos;
	
	/* true iff the world is probabilistic. If false, robot pings always return the correct value at the given position */
	private boolean isProbabilistic = false;
	
	/*Fields for GUI*/
	private GUI g;
	private boolean hasGUI;
	
	/*Whether or not world has GUI*/
	public boolean getHasGUI() {
		return this.hasGUI;
	}
	/*How long something needs to sleep*/
	private int sleepNumber;
	
	/**
	 * Constructor. Given a filename, loads in that world into the map
	 * */
	public World(String filename, boolean isProbabilistic)throws Exception{
		
		this.isProbabilistic = isProbabilistic;
				
		loadWorld(filename);
		
	}
	
	/*Method for creating GUI*/
	public void createGUI(int width, int height, int stepCounter){
		
		this.hasGUI = true;
		this.sleepNumber = stepCounter;
		
		/*Minimum sleepNumber is 100*/
		if(this.sleepNumber < 100){
			this.sleepNumber = 100;
		}
		
		g = new GUI(worldMap, this.isProbabilistic, this.sleepNumber, width, height);

	}
	
	
	/**
	 * The robot can ping the map to see what is there. However, the correct answer is not always given,
	 * especially if the position is far away from the robot
	 * */
	protected String pingMap(Robot robot, Point pingPoint){
		
		/* Make sure robot isn't null */
		if(robot == null) return null;
		
		/* Make sure new position is in bounds */
		if(pingPoint.x < 0 || pingPoint.x >= worldMap.size()) return null;
		if(pingPoint.y < 0 || pingPoint.y >= worldMap.get(0).size()) return null;
		
		/* Get the actual String at the desired position */
		String loc = worldMap.get(pingPoint.x).get(pingPoint.y);
		
		/* If loc is either 'S' or 'F' always return it */
		if(loc.equals("S")) return loc;
		if(loc.equals("F")) return loc;
		
		/* If we want to use probability version...then flip a coin and maybe change the loc value */
		if(isProbabilistic){
			
			/* Get the distance from the robot */
			int dist = Math.max(Math.abs(robot.getX() - pingPoint.x), Math.abs(robot.getY() - pingPoint.y));
			
			/* Let 8 be the "max" distance */
			int cutoff = Math.min(dist, 8);
			
			/* Rand num between 1 and 10 */
			int rand = (int)Math.floor(Math.random()*10);
			
			/* Sometimes the robot gets a random response back from the world */
			if(rand < cutoff){
				if(Math.random() < 0.5) loc = "O";
				else loc = "X";
			}
		}
		
		return loc;
	}
	
	/**
	 * Moves the robot
	 * */
	protected boolean isValidMove(Point curPos, Point newPos){
		
		
		/* Make sure new position is in bounds */
		if(newPos.x < 0 || newPos.x >= worldMap.size()) return false;
		if(newPos.y < 0 || newPos.y >= worldMap.get(0).size()) return false;
		
		/* Make sure we are only attempting to move one unit in any direction including diagonals */
		if(Math.abs(newPos.x - curPos.getX()) > 1 || Math.abs(newPos.y - curPos.getY()) > 1) return false;
		
		/* Check if the new position is valid */
		String loc = worldMap.get(newPos.x).get(newPos.y);
		
		/*Show the wall or show the grass depending*/
		if(loc.equals("X")) {
			if(g!=null){
			g.showWall(newPos);
			}
			return false;
		}
		if(g!=null){
		g.refresh(curPos, newPos);
		}
		
		return true;
	}
	
	/**
	 * Tests the end of game condition for the given robot
	 * */
	protected boolean testEndGameCondition(Robot robot){
		if(worldMap.get(robot.getX()).get(robot.getY()).equals("F")) return true;
		return false;
	}
	
	/*Sends guess info to GUI*/
	void makeGuess(Point p, boolean grass){
		this.g.makeGuess(p, grass);
	}
	
	
	
	/**
	 * Get the number of rows or columns
	 * */
	public int numRows(){return worldMap.size();}
	public int numCols(){return worldMap.get(0).size();}
	
	public Point getStartPos(){return this.startPos;}
	public Point getEndPos(){return this.endPos;}
	
	/**
	 * Loads up the world given the filename
	 * */
	private void loadWorld(String filename)throws Exception{
		
		if(filename == null) throw new Exception("[Exception] in World.java (Constructor): filename cannot be null");
		
		/* Let them know world is loading */
		System.out.println("Loading world from file: " + filename);
		
		/* Init the world object */
		worldMap = new ArrayList<ArrayList<String>>();
		
		/* Read in the file line by line and add it to the world */
		Scanner scan = new Scanner(new File(filename));
		while(scan.hasNextLine()){
			String line = scan.nextLine();
			ArrayList<String> nextRow = new ArrayList<String>();
			StringTokenizer tokenizer = new StringTokenizer(line);
			while(tokenizer.hasMoreTokens()){
				nextRow.add(tokenizer.nextToken());
			}
			System.out.println(nextRow.toString());
			worldMap.add(nextRow);
		}
		scan.close();
		
		validateWorld();
	}
	
	/**
	 * Validates the world and ensures the world is of proper format. Will throw an error and exit
	 * if any problems are found
	 * */
	private void validateWorld(){
		
		/* Let them know! */
		System.out.println("Validating the World: Checking for errors...");
		
		/* Reset the start and end pos */
		startPos = null; endPos = null;
		
		/* First, check if the world is not null */
		if(worldMap == null){
			System.err.println("[Fatal Error]: World Map was null when validating the world...exiting");
			System.exit(2);
		}
		for(ArrayList<String> row : worldMap){
			if(row == null){
				System.err.println("[Fatal Error]: At least one row in the map was null when validating the world...exiting");
				System.exit(3);
			}
		}
		
		/* Make sure the world has at least one row with at least one thing in it */
		if(worldMap.size() == 0 || worldMap.get(0).size() == 0){
			System.err.println("[Fatal Error]: Map does not have any contents...exiting");
			System.exit(4);
		}
		
		/* Now, check to make sure all the rows have the same length */
		int firstLength = worldMap.get(0).size();
		for(ArrayList<String> row : worldMap){
			if(row.size() != firstLength){
				System.err.println("[Fatal Error]: Every row in map must have the same size (must be rectangular)...exiting");
				System.exit(5);
			}
		}
		
		/* Lastly, make sure all of the strings in the world are valid and there is one start and one end */
		ArrayList<String> validChars = new ArrayList<String>();
		validChars.add("S"); validChars.add("F"); validChars.add("O"); validChars.add("X");
		int curRow = 0; int curCol = 0;
		for(ArrayList<String> row : worldMap){
			curCol = 0;
			for(String character : row){
				boolean valid = false;
				for(String validChar : validChars){
					if(character.equals(validChar)) valid = true;
				}
				if(!valid){
					System.err.println("[Fatal Error]: Map contains an invalid character (" + character + ")...exiting");
					System.exit(6);
				}
				
				if(character.equals("S")){
					if(startPos != null){
						System.err.println("[Fatal Error]: Map contains more than one starting position...exiting");
						System.exit(7);
					}
					startPos = new Point(curRow, curCol);
				}
				
				if(character.equals("F")){
					if(endPos != null){
						System.err.println("[Fatal Error]: Map contains more than one ending position...exiting");
						System.exit(8);
					}
					endPos = new Point(curRow, curCol);
				}
				
				curCol++;
			}
			curRow++;
		}
		
		/* Ensure there was at least one start and final position */
		if(startPos == null || endPos == null){
			System.out.println("[Fatal Error]: Map does have either a start or end position.");
			System.exit(9);
		}
		
		
		/* Everything seems fine */
		System.out.println("World loaded! Everything seems ok!");
	}
	
}
