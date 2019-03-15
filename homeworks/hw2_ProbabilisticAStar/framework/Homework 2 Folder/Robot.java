package world;

import java.awt.Point;

public abstract class Robot {
	
	private World world;
	private Point position;
	private int numMoves = 0;
	private int numPings = 0;

	/**
	 * Constructor...sets a default position
	 * */
	public Robot(){
		position = new Point(0,0);
	}
	
	/**
	 * Need to implement this method in subclass!
	 * */
	public abstract void travelToDestination();
	
	
	/**
	 * Adds the robot to the given world
	 * */
	public void addToWorld(World world){
		if(world == null) return;
		
		this.world = world;
		
		setPosition(world.getStartPos());
		this.numMoves = 0;
		this.numPings = 0;
	}
	/*Allows the robot to make a guess*/
	public void makeGuess(Point p, boolean grass) {
		
		if(this.world.getHasGUI()==true){
		this.world.makeGuess(p, grass);
		}
	}
	
	/**
	 * Moves the robot to the new location. Can only move if the new position is next to your current
	 * position. Returns the new position of the robot.
	 * @throws InterruptedException 
	 * */
	public Point move(Point newPosition) {
		
		
		if(newPosition == null) return new Point(position.x, position.y);
		
		if(world.isValidMove(this.getPosition(), newPosition)){
			this.setPosition(newPosition);
			numMoves++;
			
			/* See if the game is over */
			if(world.testEndGameCondition(this)) endGame();
		}
		
		return new Point(position.x, position.y);
	}
	
	/**
	 * Ping the map to see what is there. If the world is probabilistic (see World constructor), then
	 * this return value may be incorrect.
	 * */
	public String pingMap(Point position){
		if(position == null) return null;
		
		numPings++;
		return world.pingMap(this, position);
	}
	
	/**
	 * Pings the world to see if that position has an X or an O
	 * The world sometimes returns the wrong result
	 * */
	
	
	/**
	 * The private setter for the position (internal use only)
	 * */
	private void setPosition(Point p){
		if(this.world == null) return;
		
		if(p.x < 0 || p.x >= world.numRows()) return;
		if(p.y < 0 || p.y >= world.numCols()) return;
		
		position.setLocation(p.x, p.y);
	}
	
	private void endGame(){
		
		System.out.println("You reached the destination!");
		System.out.println("Total number of moves: " + this.getNumMoves());
		System.out.println("Total number of pings: " + this.getNumPings());
		System.exit(0);
	}
	
	/**
	 * Stat getters
	 * */
	public int getNumMoves(){return numMoves;}
	public int getNumPings(){return numPings;}
	
	/**
	 * Position Getters
	 * */
	public int getX(){return getPosition().x;}
	public int getY(){return getPosition().y;}
	public Point getPosition(){return new Point(this.position.x, this.position.y);}
}
