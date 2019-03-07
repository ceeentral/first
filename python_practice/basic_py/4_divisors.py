num = int(raw_input("please input a number: "))
l1 = []
for i in range(2, num):
	if int(num) % i == 0:
		l1.append(i)
print l1
#https://www.practicepython.org/exercise/2014/02/26/04-divisors.html