__author__ = '3tral'
import random

a = random.sample(range(1,100), random.randint(1,10))
print a
def stripe(lis):
    b = [lis[0], lis[-1]]
    if b[0] == b[-1]:
        b = [b[0]]
    return b
print stripe(a)

#clean answer
##def list_ends(a_list):
##    return [a_list[0], a_list[len(a_list)-1]]


#https://www.practicepython.org/exercise/2014/04/25/12-list-ends.html