package world;
import java.awt.Component;
import java.awt.GridLayout;
import java.awt.Image;
import java.awt.Point;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import java.util.ArrayList;

import javax.imageio.ImageIO;
import javax.swing.*;
import javax.swing.border.BevelBorder;
public class GUI {

	/*The Images*/
	private Image grass;
	private Image robot;
	private Image wall;
	private Image goal;
	private Image questionmark;
	private Image lavaQuestionMark;
	private Image grassQuestionMark;

	/*map and Player data*/
	private ArrayList<ArrayList<String>> mapData;
	private Point player;

	/*Sleep Number (like the bed! Get it? No? Oh, you do. Funny right? No?*/
	private int sleepNumber;

	/*JFrame and JPanel setup*/
	JFrame frame = new JFrame("Homework 2");
	JPanel panel;

	/*Constructor for GUI*/
	public GUI(ArrayList<ArrayList<String>> worldMap, boolean uncertainty, int sleepNumber, int daWidth, int daHeight){
		
		/*Create the panel given the size of the grid*/
		panel = new JPanel(new GridLayout(worldMap.size(),worldMap.get(0).size(),0,0));
		
		/*sleepNumber*/
		this.sleepNumber = sleepNumber;

		/*Grab mapdata if not uncertain*/
		if(!uncertainty){
			mapData = (ArrayList<ArrayList<String>>) worldMap.clone();
		}
		
		else{
			mapData = new ArrayList<ArrayList<String>>();
		}

		/*Read in all of the image files*/
		try {
			grass = ImageIO.read(new File("guiImages/open.png")).getScaledInstance(daWidth / worldMap.get(0).size(), daHeight/ worldMap.size(), Image.SCALE_SMOOTH);
			robot = ImageIO.read(new File("guiImages/robot.png")).getScaledInstance(daWidth / worldMap.get(0).size(), daHeight/ worldMap.size(), Image.SCALE_SMOOTH);;
			goal = ImageIO.read(new File("guiImages/goal.png")).getScaledInstance(daWidth / worldMap.get(0).size(), daHeight/ worldMap.size(), Image.SCALE_SMOOTH);;
			wall = ImageIO.read(new File("guiImages/closed.png")).getScaledInstance(daWidth / worldMap.get(0).size(), daHeight/ worldMap.size(), Image.SCALE_SMOOTH);;
			questionmark = ImageIO.read(new File("guiImages/unknown.png")).getScaledInstance(daWidth / worldMap.get(0).size(), daHeight/ worldMap.size(), Image.SCALE_SMOOTH);;
			lavaQuestionMark = ImageIO.read(new File("guiImages/closedguess.png")).getScaledInstance(daWidth / worldMap.get(0).size(), daHeight/ worldMap.size(), Image.SCALE_SMOOTH);;
			grassQuestionMark = ImageIO.read(new File("guiImages/openguess.png")).getScaledInstance(daWidth / worldMap.get(0).size(), daHeight/ worldMap.size(), Image.SCALE_SMOOTH);;
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}

		/*Builds the images to add to the GridLayout*/
		for (int i = 0; i <worldMap.size(); i++){
			
			ArrayList<String> temp = new ArrayList<String>();
			
			for(int j = 0; j < worldMap.get(i).size(); j++){

				String s = worldMap.get(i).get(j);
				ImageIcon p;


				if(s.equals("S")){	
					p = new ImageIcon(robot);
					temp.add("S");
					player = new Point(i,j);	
				}
				else if(s.equals("F")){	
					p = new ImageIcon(goal);
					temp.add("F");	
				}
				else if(uncertainty){
					p = new ImageIcon(questionmark);
					temp.add("?");
				}
				else{
					if(s.equals("X")){
						p = new ImageIcon(wall);
					}
					else{
						p = new ImageIcon(grass);

					}
				}


				JLabel pic = new JLabel(p);
				panel.add(pic);

			}

			mapData.add(temp);

		}
		
		/*Adds the panel to the frame, sets the dimensions and makes it visible*/

		frame.setContentPane(panel);
		frame.setSize(daWidth,daHeight);
		frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		frame.setVisible(true);
	}
	
	/*Update the GUI to reflect the guess of the robot for a specific square*/
	public void makeGuess(Point p, boolean grass){

		try {
			Thread.sleep(this.sleepNumber);
		} catch (InterruptedException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}

		/*Remove the current image icon and add the appropriate guess one*/
		int guessLoc = (mapData.get(0).size()*p.x + p.y);
		panel.remove(guessLoc);
		JLabel guessLabel;
		if(grass){
			guessLabel = new JLabel(new ImageIcon(grassQuestionMark));
		}
		else{
			guessLabel = new JLabel(new ImageIcon(lavaQuestionMark));
		}

		panel.add(guessLabel,guessLoc);
		panel.revalidate();
		panel.repaint();

	}

	/*Show the wall if the robot bumps into it*/
	public void showWall(Point wallP){

		try {
			Thread.sleep(this.sleepNumber);
		} catch (InterruptedException e) {
			e.printStackTrace();
		}

		if(mapData.get(wallP.x).get(wallP.y).equals("?")){
			int wallLoc = (mapData.get(0).size()*wallP.x)+wallP.y;
			panel.remove(wallLoc);
			JLabel wally = new JLabel(new ImageIcon(wall));
			panel.add(wally, wallLoc);
			panel.revalidate();
			panel.repaint();	
			ArrayList<String> temp = new ArrayList<String>();
			temp = mapData.get(wallP.x);
			temp.set(wallP.y, "X");
			mapData.set(wallP.x, temp);
		}
	}

	public void refresh(Point curr, Point old){

		try {
			Thread.sleep(this.sleepNumber);
		} catch (InterruptedException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}

		int newRobotIndex = (mapData.get(0).size()*curr.x)+curr.y;
		int oldRobotIndex = (mapData.get(0).size()*old.x)+old.y;

		panel.remove(newRobotIndex);
		JLabel grassy = new JLabel(new ImageIcon(grass));
		panel.add(grassy, newRobotIndex);

		panel.remove(oldRobotIndex);
		JLabel roboty = new JLabel(new ImageIcon(robot));
		panel.add(roboty, oldRobotIndex);

		panel.revalidate();
		panel.repaint();	


	}
	public void moveRobot(Point p){
		//Set the current position of the player to be open
		ArrayList<String> temp = mapData.get(player.x);
		temp.set(player.y, "O");
		mapData.set(player.x, temp);

		//Set the new position of the player
		temp = mapData.get(p.x);
		temp.set(p.y, "S");
		mapData.set(p.x, temp);

		refresh(p,player);

		player.x = p.x;
		player.y = p.y;

	}
}
