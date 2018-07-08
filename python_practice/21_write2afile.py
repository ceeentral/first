__author__ = '3tral'
with open('file_to_write.txt', 'w') as open_file:
	open_file.write('A string is your mom')
	open_file.write("\nhow's your single day?")

open_file = open('s2ndfile.txt','w')
open_file.write('laozi shi dier pa')
open_file.close()

#reading file official web https://docs.python.org/3.3/tutorial/inputoutput.html#reading-and-writing-files

#https://www.practicepython.org/exercise/2014/11/30/21-write-to-a-file.html