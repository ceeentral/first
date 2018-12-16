//declare int array to hold th locatin cell
//declare int to count hits times. set to 0

//declare checkYorself() method to take the guess of users, check it and return a result reprsenting a 'hit', 'miss', 'kill'

//declare  setLocationCells() setter method take an int array which has 3 cell location as int

//////////////////
public String checkYorself(String[] userGuess) {
	int guess = Interger.parseInt(userGuess);
	String result = 'miss';
	for (int cell : locationCells) {
		if ( guess == cell) {
			result = 'hit';
			numofHits++;
			break;

		}
	}
	if (numofHits == locationCells.lenth) {
		result = 'kill';

	}
	System.out.println(result);
	return result;
}
	//get the user guess as a String Para
	//Conver the user guess to an int 
	//repeat each of the location cells in the int array
		//compare the user guess to the location cell 
		//if the user guess matches
			//increment the number of this
			//find out if it was the last location cell:
				//if number of the hit is 3 return 'kill'
				//else it was not a kill so return 'hit' along with increment number
			//end if 
		//else the user guess didn't match so return 'miss'
		//end if 
	//end repeat
//end method


//method void setLocationCells(int[] celllocations)
	//get the cell locations as an int array pata
	//assign the cell locations para to the cell olocations instance variable
//end method
