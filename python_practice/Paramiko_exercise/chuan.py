# exercise for fun.
#and please use python3+
import os
import sys
from sshnew import *
from ipnew import *

print("this is the new try, and i decide to use py3")
print("and i find that, if i import the 2 file above 'ipnew & sshnew', it will create xx.pyc automaticlly.")
print("next work is trans sshnew & ipnew from py2 to py3")

#loginSSH_test(chigago)
#execCommand(chigago,"ls -al")
#execCommand_security(chigago, "ls -alh")
#xecCommands(chigago, ["echo 'new try'>>aa.txt"])
#execCommand(chigago, "cat aa.txt")
#downloadFile(chigago, '/root/aa.txt', '/Users/central/ggit/first/python_practice/Paramiko_exercise/aa.txt')
uploadFile(chigago, '/Users/central/ggit/first/python_practice/Paramiko_exercise/bb.txt', '/root/bb.txt')
execCommands(chigago, ["ls -alh"])
