__author__ = '3tral'
def reverorder():
	st = raw_input("please input a string you want to reverse:\n")
	result = st.split()
	ab = st.split()[::-1]
	return ab
print reverorder()
#but my result is a list format, not a string format. it's not big deal, but i care.
#so it can be change like the answer:
# return ' '.join(ab)

# clean answer:
def reverseWord(w):
  return ' '.join(w.split()[::-1])

#another answer:
def reverse_v1(x):
  y = x.split()
  result = []
  for word in y:
    result.insert(0,word)  #always insert the words at list[0]  
  return " ".join(result)
def reverse_v4(x):
  y = x.split()
  y.reverse()  #python already builtin the function
  return " ".join(y)
#https://www.practicepython.org/exercise/2014/05/21/15-reverse-word-order.html