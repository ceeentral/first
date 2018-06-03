l1 = [1, 5, 23, 67, 546, 999]
print l1
l2 = []
for i in l1:
	if i <= 10:
		
		l2.append(i)
#extra-1

print l2
l3 = []
num =  raw_input("enter a number: ")
for i in l1:
	if i <= int(num):
		l3.append(i)
print l3

#extra-2+3	
number = raw_input("enter a number: ")
print(list(filter(lambda x: (x <= int(number)), l1)))

#https://www.practicepython.org/exercise/2014/02/15/03-list-less-than-ten.html