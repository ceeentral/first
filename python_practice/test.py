a = raw_input("input a number:\n")
i = 5
print ("tried %d" %i)
if a == 'exit':
	exit('user end the game.')
else:
	if int(a) not in range(1,5):
		print "goof"
	else:
		print "genius"