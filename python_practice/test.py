p1 = raw_input("what's your request?\n\n").lower()
p2 = raw_input("what's your request?\n\n").lower()

choices = list(['papper', 'rock', 'scissors'])

if p1 not in choices:
	print("you a goof")
if p2 not in choices:
	print("you a goof")
if p1 == p2:
	print("it's a draw")
if choices.index(p1) == (choices.index(p2) + 1 ) % 3:
	print ("player 2 wins!")
if choices.index(p2) == (choices.index(p1) + 1 ) % 3:
	print ("player 1 wins!")
print choices.index(p1)
print choices.index(p2)