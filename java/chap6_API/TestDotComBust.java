public class DotComBustTestDrive {
	public static void main (String[] args) {
		DotComBust newone = new DotComBust(); //初始化一个DotComBust对象
		GameHelper help = new GameHelper(); //初始化一个GameHelper对象

		newone.setUpGame(); //设置初始DotCom的位置
		String userGuess = A5 //猜测 这里如何做到循环输入呢？？？
		help.input(String userGuess); 
		newone.startPlaying(); //开始游戏, startPlay会去主动调用checkUserGuess函数
		newone.finishGame();


	}
}
