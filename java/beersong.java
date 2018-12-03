public class beersong {
	public static void main (String[] args) {
		int beerNem = 99;
		String word = "bottles";
		while (beerNem >0) {
				if (beerNem == 1) {
					word = "bottle";
				}
				System.out.println(beerNem + " " + word + " of beer on the wall");
				System.out.println(beerNem + " " + word + " of beer.");
				System.out.println("Take one down.");
				System.out.println("Pass it around.");
				beerNem = beerNem - 1;
				if (beerNem > 0) {
					System.out.println(beerNem + " " + word + " of beer on the wall");
				}else {
					System.out.println("No more bottles of beer on the wall");
				}
		}
	}
}