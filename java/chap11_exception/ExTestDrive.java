import static java.lang.System.out;
class MyEx extends Exception {}
public class ExTestDrive {
	public static void main(String [] args) {
		String test = args[0];
		try {
			out.print("t");
			doRisky(test);
			out.print("o");
		}catch (MyEx e) {
			out.print("a");
		}finally {
			out.print("w");
		}
		out.println("s");
	}
	static void doRisky(String t) throws MyEx {
		out.print("h");
		if ("yes".equals(t)) {
			throw new MyEx();
		}
		out.print("r");
	}
}