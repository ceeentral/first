#come and guess number
__author__ = '3tral'
import random
a = random.randint(1,10)
print a
guessnum = raw_input("please input your guess number:\nrange from 1-10\n")
def guessfunc(num):
    if num.isdigit():
        if int(num) not in range(1,11):
            if int(num) == a:
                print ("Bingo! genius. it is " + str(a) )
                #exit
            if int(num) < a:
                num = raw_input("it's less, guess higher.\n")
                guessfunc(num)
            if int(num) > a:
                num = raw_input("it's more, guess lower.\n")
                guessfunc(num)
        else:
            print "you a goof"
    else:
        print "you a goof"
guessfunc(guessnum)