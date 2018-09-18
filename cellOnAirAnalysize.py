#!/usr/bin/python	
__author__ = '3tral'

import os
import time

def bash_haha(bash_command):
	#used for execute bash command. implements interactive between python and bash.
	#strip() means delete space around the head and the tail
	try:
		return os.popen(bash_command).read().strip()
	except:
		return None
print(bash_haha('pwd'))
#for unzip the file
#unzip log.zip -d /tmp
#unzip log.zip -d /tmp/chuan |tar zxvf /tmp/chuan/du.tgz -C /tmp/chuan

