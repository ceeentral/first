__author__ = '3tral'
s1 = raw_input("please input a sting: ")
def reverse(abc):

	a = len(abc)
	print a
	b = ''
	for i in range(0, a):
		b += abc[a-1-i]
	return b
x = reverse(s1)
print x
if x == s1:
	print (s1 + " is a palindrome")
else:
	print (s1 + " is not a palindrome")
#https://www.practicepython.org/exercise/2014/03/12/06-string-lists.html

#or you can try below one

#wrd=input("Please enter a word")
#wrd=str(wrd)
#rvs=wrd[::-1]
#print(rvs)
#if wrd == rvs:
#    print("This word is a palindrome")
#else:
#    print("This word is not a palindrome")