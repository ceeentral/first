# -*- coding:utf-8 -*-
#2018-02-11 created by Yang Liyong A
#2018-02-12 modified by Yang Liyong A, add new func "loginSSH_test"
#2018-02-13 add func "execCommand"
#2018-03-02 add func "downloadFile_security", "execCommands_security" and "execCommand_security"
#2018-10-24 modify by Wang jianfeng ，modify ip get method using ConfigParser lib

import paramiko
import threading
import configparser,os

def loginSSH_enable(SSHInfo):
    #print "start to test", SSHInfo
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(SSHInfo["ip"],username=SSHInfo["user"],password=SSHInfo["password"])
        client.close()
    except:
        print("SSH login fail, IP is ", SSHInfo["ip"], "username is ", SSHInfo["user"], "password is", SSHInfo["password"])
        return False
    return True

def loginSSH_test(SSHInfo):
    #print "start to test", SSHInfo
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(SSHInfo["ip"],username=SSHInfo["user"],password=SSHInfo["password"])
        client.close()
    except:
        print("SSH login fail, IP is ", SSHInfo["ip"], "username is ", SSHInfo["user"], "password is", SSHInfo["password"])
        return False
    return True

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

def execCommands_security(SSHInfo, commands): #2018-03-02 add
    if loginSSH_test(SSHInfo):
        execCommands(SSHInfo, commands)

def execCommand(SSHInfo, command): #2018-02-13 add
    client=loginSSH(SSHInfo)
    print("success to ssh to "+SSHInfo["ip"])
    #for command in commands:
    print(command)
    stdin,stdout,stderr = client.exec_command(command)
        #if "ssh" in command:
        #    continue
        #print stderr.readlines()
    result=stdout.readlines()
    for line in result:    #delete print 2018-03-02
        print(line),        #delete print 2018-03-02
    client.close()
    return result

def execCommand_security(SSHInfo, command): #2018-03-02 add
    result =[]
    #return result
    if loginSSH_test(SSHInfo):
        result = execCommand(SSHInfo, command)
    return result

def loginSftp(SSHInfo):
    tran = paramiko.Transport((SSHInfo["ip"],22))
    tran.connect(username = SSHInfo["user"], password = SSHInfo["password"])
    sftp = paramiko.SFTPClient.from_transport(tran)
    return tran, sftp

def uploadFile(SSHInfo, localpath, remotepath):
    print("try to upload "+localpath+" to "+SSHInfo["ip"])
    tran, sftp = loginSftp(SSHInfo)
    #uploadFile(sftp, localpath, remotepath)
    sftp.put(localpath,remotepath)
    print("success to upload "+localpath+" to "+SSHInfo["ip"])
    #downloadFile
    tran.close()

def downloadFile(SSHInfo, remotepath, localpath):
    print("try to download "+remotepath+" from "+SSHInfo["ip"])
    tran, sftp = loginSftp(SSHInfo)
    #uploadFile(sftp, localpath, remotepath)
    sftp.get(remotepath, localpath)
    print("success to download "+localpath+" from "+SSHInfo["ip"])
    #downloadFile
    tran.close()

def downloadFile_security(SSHInfo, remotepath, localpath): #2018-03-02 add
    fName = remotepath.split("/")[-1]
    remotefolder = remotepath[:(0-len(fName))]
    localfolder=localpath[:(0-len(fName))]
    #print remotefolder,fName
    results = execCommand_security(SSHInfo, "ls -l "+remotefolder)
    #print results
    for line in results:
        if fName in line:
            f = line.split()[-1]
            #airphone L1
            try:
                downloadFile(SSHInfo, remotefolder+f, localfolder + f)
            except Exception as e:
                print("Error: download file error: ", e)


def get_configInfo(options,target):

    cf = configparser.SafeConfigParser()
    cf.read(os.getcwd() + r'\config\config.ini')
    config = cf.get(options, target)
    return config

# override threading
class MyThread(threading.Thread):

    def __init__(self,target,args):
        threading.Thread.__init__(self)
        self._target = target
        self._arg = args
    def run(self):
        self._target(*self._arg)
