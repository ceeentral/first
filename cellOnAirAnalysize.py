#!/usr/bin/python	
__author__ = 'Central Wang'

import os
import time
import mmap

def prepare_log():
	########check path and target log valid or not.
	if os.path.exists('/tmp/123chuan'):
		pass
	else:
		os.mkdir('/tmp/123chuan')
	if os.path.exists('log.zip'):
		pass
	else:
		print "you must use shell script to get log.zip first"
		exit()
	#####unzip target logs and prepare for check key words for cell setup.
	a=os.system('unzip -o log.zip -d /tmp/123chuan |tar zxvPf /tmp/123chuan/du.tgz -C /tmp/123chuan >>/dev/null 2>&1')
	if a==0:
		if os.path.exists('/tmp/123chuan/startup_DEFAULT.log.xz'):
			os.system('xz -d /tmp/123chuan/startup_DEFAULT.log.xz')
		
		print "unzip successfully"
	else:
		print "something wrong with zip"
	#####double check if there is log we're looking for.
	if os.path.exists('/tmp/123chuan/startup_DEFAULT.log'):
		pass
	else:
		print "please check your log.zip, there is no cprt log"
		exit()


CPRT_CM_CONFIGURATION=['CPRT_CM_CONFIGURATION_REQ_MSG', 'CPRT_CM_CONFIGURATION_RESP_MSG']
CPRT_CM_NETWORK_PLAN=['CPRT_CM_NETWORK_PLAN_REQ_MSG', 'CPRT_CM_NETWORK_PLAN_RESP_MSG', 'CPRT_CM_NETWORK_PLAN_ACTIVATION_COMPLETE_IND_MSG']
CPRT_CM_POOL_CONFIGURATION=['CPRT_CM_POOL_CONFIGURATION_REQ_MSG', 'CPRT_CM_POOL_CONFIGURATION_RESP_MSG']
CPRT_CM_CELL_MAPPING=['CPRT_CM_CELL_MAPPING_REQ_MSG', 'CPRT_CM_CELL_MAPPING_RESP_MSG']
F1AP=['Task 1 end successfully!', 'Task 2 end successfully!']
CU_MSG=['Received gnb cu configuration update from CU']
L1_CELL_SETUP=['Sending message with msgId= 0x21a to sicad', 'Receiving message with msgId= 0x201 from sicad', 'Sending message with msgId= 0x110 to sicad', 'Receiving message with msgId= 0x101 from sicad']
Lo_CELL_SETUP=['Sending message with msgId= 0x820 to sicad', 'Receiving message with msgId= 0x821 from sicad']
PS_CELL_SETUP=[' Sending message with msgId= 0x920 to sicad' 'Receiving message with msgId= 0x921 from sicad']
DU_MSG=['Sending message with msgId= 0xf1f3 to sicad']

def checklog(part):
    for i in part:
	f = open('/tmp/123chuan/startup_DEFAULT.log')
        s = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        if s.find(i) != -1:
            print( i )
        else:
            print ("problem came out at " + i)
            return "failed"
mod=[CPRT_CM_CONFIGURATION, CPRT_CM_NETWORK_PLAN, CPRT_CM_POOL_CONFIGURATION, CPRT_CM_CELL_MAPPING, F1AP, CU_MSG, L1_CELL_SETUP, Lo_CELL_SETUP, PS_CELL_SETUP, DU_MSG]
def execute():
    for b in mod:
	    if checklog(b)=='failed':
	        print "something wrong in " +  str(b)
		return "not good"
if execute()=='not good':
	pass
else:
	print 'your gnb looks fine with cell on air'
