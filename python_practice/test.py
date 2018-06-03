__author__ = '3tral'

__author__ = '3tral'

print "welcome to the hotest ROCK PAPER SCISSORS all over the world"
#p1 = ''
#p2 = ''
#def startgame():
para1 = raw_input("Player1,please input your gesture: \nr for ROCK,\np for PAPER,\ns for SCISSORS\n")
para2 = raw_input("Player2,please input your gesture: \nr for ROCK,\np for PAPER,\ns for SCISSORS\n")
	#p1 = a1
	#p2 = a2
#def rackpaperscissors(para1, para2):
if para1 == 'r':
	if para2 == 'r':
		print "you play even"
		a = raw_input("start a new game? (y/n)")
		if a == 'y':
			print "hah"#startgame()
		else:
			pass
	if para2 == 's':
		print "player1 win!"
	if para2 == 'p':
		print "player2 win!"
	if para2 != 'r' or 's' or 'p':
		print "idiot!"
if para1 == 's':
	if para2 == 'r':
		print "player2 win!"
	if para2 == 's':
		print "you play even"
		a = raw_input("start a new game? (y/n)")
		if a == 'y':
			print "hah"#startgame()
		else:
			pass
	if para2 == 'p':
		print "player1 win!"
	if para2 != 'r' or 's' or 'p':
		print "idiot!"
if para1 == 'p':
	if para2 == 'r':
		print "player1 win!"
	if para2 == 's':
		print "player2 win!"
	if para2 == 'p':
		print "you play even"
		a = raw_input("start a new game? (y/n)")
		if a == 'y':
			print "haha"#startgame()
		else:
			pass
	if para2 != 'r' or 's' or 'p':
		print "idiot!"
if para1 != 'r' or 's' or 'p':
		print "idiot!"
				
#startgame()
#rackpaperscissors(p1, p2)

#https://www.practicepython.org/exercise/2014/03/26/08-rock-paper-scissors.html



