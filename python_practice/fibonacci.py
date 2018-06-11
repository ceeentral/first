__author__ = '3tral'
num = raw_input("please give a number of numbers for Fibonacci:\n")

def fibonacci(nums):
    a = [1, 1]
    print a 
    for(i=2;i<nums;i++):
        a[i] = a[i-1] + a[i-2]
        a.append(a[i])
    print a
