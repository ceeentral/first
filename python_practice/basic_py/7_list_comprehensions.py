__author__ = '3tral'
a = [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
b = []
for i in a:
	if i % 2 ==0:
		b.append(i)

print b

#but have to write in a line. so it should be:
c = [i for i in a if i % 2 == 0]
print c


#another way to create random lenth list and random content list


#import random
#
#numlist = []
#list_length = random.randint(5,15)
#
#
#while len(numlist) < list_length:
#    numlist.append(random.randint(1,75))
#    
#
#evenlist = [number for number in numlist if number % 2 == 0] 
#
#print(numlist)
#print(evenlist)

#https://www.practicepython.org/exercise/2014/03/19/07-list-comprehensions.html