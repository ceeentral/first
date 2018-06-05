__author__ = '3tral'

print "welcome to the hotest ROCK PAPER SCISSORS all over the world"
#p1 = ''
#p2 = ''
def startgame():
	global p1
	p1 = raw_input("Player1,please input your gesture: \nr for ROCK,\np for PAPER,\ns for SCISSORS\n")
	global p2

	p2 = raw_input("Player2,please input your gesture: \nr for ROCK,\np for PAPER,\ns for SCISSORS\n")
	#return pp1, pp2

	#p1 = a1
	#p2 = a2
def rackpaperscissors(para1, para2):
	if para1 == 'r':
		if para2 == 'r':
			print "you play even"
			a = raw_input("start a new game? (y/n)")
			if a == 'y':
				print 'hah, idiot.'
				startgame()
			else:
				pass
		if para2 == 's':
			print "player1 win!"
		if para2 == 'p':
			print "player2 win!"
	if para1 == 's':
		if para2 == 'r':
			print "player2 win!"
		if para2 == 's':
			print "you play even"
			a = raw_input("start a new game? (y/n)")
			if a == 'y':
				startgame()
			else:
				pass
		if para2 == 'p':
			print "player1 win!"
	if para1 == 'p':
		if para2 == 'r':
			print "player1 win!"
		if para2 == 's':
			print "player2 win!"
		if para2 == 'p':
			print "you play even"
			a = raw_input("start a new game? (y/n)")
			if a == 'y':
				startgame()
			else:
				pass
				
#p1, p2= startgame(p1, p2)
startgame()
print p1
print p2
rackpaperscissors(p1, p2)

#https://www.practicepython.org/exercise/2014/03/26/08-rock-paper-scissors.html

