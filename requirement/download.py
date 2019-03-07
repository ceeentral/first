#this is based on yly's python script and combine my self's shell script.
#2018-11-09 done this version.

import paramiko
import time
import os
from scp import SCPClient
import sys

print("this is the start: "+ time.ctime())

current_folder=os.getcwd()
gNB_OAM_SSHInfo={"ip":"10.57.207.8","user":"robot","password":"rastre1"}
#gNB_Asik_SSHInfo={"ip":"10.57.233.139","user":"toor4nsn","password":"oZPS0POrRieRtu"}
#gNB_RU_SSHInfo={"ip":"10.10.10.10","user":"root","password":"umniedziala"}

def uploadFile(SSHInfo, localpath, remotepath):
    print("try to upload "+localpath+" to "+SSHInfo["ip"])
    tran, sftp = loginSftp(SSHInfo)
    #uploadFile(sftp, localpath, remotepath)
    sftp.put(localpath,remotepath)
    print("success to upload "+localpath+" to "+SSHInfo["ip"])
    #downloadFile
    tran.close()


def loginSSH(SSHInfo):
	print("try to ssh to "+SSHInfo["ip"])
	client = paramiko.SSHClient()
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	client.connect(SSHInfo["ip"],username=SSHInfo["user"],password=SSHInfo["password"])
	return client



def execCommands(SSHInfo, commands):
	client=loginSSH(SSHInfo)
	print("success to ssh to "+SSHInfo["ip"])
	for command in commands:
		print(command)
		stdin,stdout,stderr = client.exec_command(command)
		#if "ssh" in command:
		#    continue
		#print stderr.readlines()
		for line in stdout.readlines():
			print(line, end=' ')
	client.close()



def loginSftp(SSHInfo):
	tran = paramiko.Transport((SSHInfo["ip"],22))
	tran.connect(username = SSHInfo["user"], password = SSHInfo["password"])
	sftp = paramiko.SFTPClient.from_transport(tran)
	return tran, sftp


def downloadFile(SSHInfo, remotepath, localpath):
	print("try to download "+remotepath+" from "+SSHInfo["ip"])
	tran, sftp = loginSftp(SSHInfo)
	#uploadFile(sftp, localpath, remotepath)
	sftp.get(remotepath, localpath)
	print("success to download "+localpath+" from "+SSHInfo["ip"])
	#downloadFile
	tran.close()

uploadFile(gNB_OAM_SSHInfo, "collect.sh", "/home/robot/collect.sh" )
execCommands(gNB_OAM_SSHInfo, ["bash collect.sh"])

log_dir_name="log_"+time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
os.mkdir(log_dir_name)
downloadFile(gNB_OAM_SSHInfo, "log.zip", current_folder+"/"+log_dir_name+"/"+"log.zip")
print("this is the end: "+ time.ctime())
