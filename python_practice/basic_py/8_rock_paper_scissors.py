__author__ = '3tral'

print "welcome to the hotest ROCK PAPER SCISSORS all over the world"

def startgame():
	global p1
	p1 = raw_input("Player1,please input your gesture: \nr for ROCK,\np for PAPER,\ns for SCISSORS\n")
	global p2

	p2 = raw_input("Player2,please input your gesture: \nr for ROCK,\np for PAPER,\ns for SCISSORS\n")

def rockpaperscissors(para1, para2):
	if para1 == 'r':
		if para2 == 'r':
			print "draw"
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
			print "draw"
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
			print "draw"
			a = raw_input("start a new game? (y/n)")
			if a == 'y':
				startgame()
			else:
				pass
				
startgame()
print p1
print p2
rockpaperscissors(p1, p2)
    

#https://www.practicepython.org/exercise/2014/03/26/08-rock-paper-scissors.html



#p1 = raw_input("what's your request?\n\n").lower()
#p2 = raw_input("what's your request?\n\n").lower()
#
#choices = list(['papper', 'rock', 'scissors'])
#
#if p1 not in choices:
#	print("you a goof")
#if p2 not in choices:
#	print("you a goof")
#if p1 == p2:
#	print("it's a draw")
#if choices.index(p1) == (choices.index(p2) + 1 ) % 3:
#	print ("player 2 wins!")
#if choices.index(p2) == (choices.index(p1) + 1 ) % 3:
#	print ("player 1 wins!")
##python 中有list index和字符串index， 详情可见 
##http://www.runoob.com/python/att-string-index.html
##http://www.runoob.com/python/att-list-index.html
