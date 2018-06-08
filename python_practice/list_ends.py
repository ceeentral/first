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


