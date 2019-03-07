__author__ = '3tral'
import random

def pwgen():
  letterlt = 'abcdefghijklmnopqrstuvwxyzABC,.;'
  pw = ''
  for i in range(8):
    pw += random.choice(letterlt)
  print pw
pwgen()


###answer from internet
##import string
##import random
##characters = string.ascii_letters + string.punctuation  + string.digits
##password =  "".join(random.choice(characters) for x in range(random.randint(8, 16)))
##print password
##
###but i didn't check the capital and nurmerial, so need to update.
#https://www.practicepython.org/exercise/2014/05/28/16-password-generator.html