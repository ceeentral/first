#come and guess number
__author__ = '3tral'
import random
a = random.randint(1,10)
print a
guessnum = raw_input("please input your guess number:\nrange from 1-10\n")
counter = 0
def guessfunc(num):
    global counter 
    counter += 1
    if num == 'exit':
        exit('User ended the game.')
    else:
        if num.isdigit():
            if int(num) in range(1,11):
                if int(num) == a:
                    print ("Bingo! genius. it is " + str(a) )
                    print ("you've tried %d times" %counter)
                if int(num) < a:
                    num = raw_input("it's less, guess higher.\n")
                    guessfunc(num)
                if int(num) > a:
                    num = raw_input("it's more, guess lower.\n")
                    guessfunc(num)
            else:
                print "you a goof"
                guessnum = raw_input("please input your guess number:\nrange from 1-10\n")
                guessfunc(guessnum)
        else:
            print "you a big goof"
            guessnum = raw_input("please input your guess number:\nrange from 1-10\n")
            guessfunc(guessnum)
guessfunc(guessnum)

#https://www.practicepython.org/exercise/2014/04/02/09-guessing-game-one.html