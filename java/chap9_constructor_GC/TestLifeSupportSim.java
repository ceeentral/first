import java.util.*;
class V2Radiator {
	V2Radiator(ArrayList list) {
		for(int x=0; x<5; x++) {
			list.add(new SimUnit("V2Radiator"));
		}

	}
}
class V3Radiator extends V2Radiator {
	V3Radiator(ArrayList lglist) {
		super(lglist);
		for(int g=0; g<10; g++) {
			lglist.add(new SimUnit("V3Radiator"));
		}
	}
}
class RetentionBot {
	RetentionBot(ArrayList rlist) {
		rlist.add(new SimUnit("Retention"));
	}
}
public class TestLifeSupportSim {
	//@SuppressWarnings("unchecked")
	public static void main(String [] args) {
		ArrayList<String> aList = new ArrayList<String>();
		V2Radiator v2 = new V2Radiator(aList);
		System.out.println(v2);
		V3Radiator v3 = new V3Radiator(aList);
		for(int z=0; z<20; z++) {
			RetentionBot ret = new RetentionBot(aList);
		}
	}
}
class SimUnit {
	String botType;
	SimUnit(String type) {
		botType = type;
		System.out.println(botType);
	}
	int powerUse() {
		if ("Retention".equals(botType)) {
			return 2;
		}
		else {
			return 4;
		}
	}
	
}
