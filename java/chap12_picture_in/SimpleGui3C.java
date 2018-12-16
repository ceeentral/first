import javax.swing.*;
import java.awt.event.*;
import java.awt.*;
public class SimpleGui3C implements ActionListener {
	JFrame frame;
	public static void main(String [] args) {
		SimpleGui3C gui = new SimpleGui3C();
		gui.go();
	}
	public void go() {
		frame = new JFrame();
		JButton button = new JButton("change color");
		button.addActionListener(this);
		
		frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		MyDrawPanel drawPanel = new MyDrawPanel();
		frame.getContentPane().add(BorderLayout.NORTH, button);
		frame.getContentPane().add(BorderLayout.CENTER, drawPanel);
		frame.setSize(300,300);
		frame.setVisible(true);
	}
	public void actionPerformed(ActionEvent event) {
		frame.repaint();
	}
}
class MyDrawPanel extends JPanel {
	public void paintComponent(Graphics g) {}
}