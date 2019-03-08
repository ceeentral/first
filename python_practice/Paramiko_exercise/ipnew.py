#2018-02-24 created by Yang Liyong A

gNB_OAM_SSHInfo={"ip":"10.57.203.2","user":"robot","password":"xx"}
gNB_Asik_SSHInfo={"ip":"192.168.255.1","user":"aa","password":"xx"}
gNB_RRU_SSHInfo={"ip":"192.168.100.5","user":"root","password":"aa"}

gNB_BB2_SSHInfo={"ip":"1.1.1.1","user":"_rcpadmin","password":"RCP_owner"}
gNB_Asia_SSHInfo={"ip":"192.168.2.60","user":"aa","password":"xx"}

ftp_SSHInfo={"ip":"10.56.6.5","user":"tdlte","password":"tdlte"}

airphone_OAM_SSHInfo={"ip":"135.251.156.36","user":"xx","password":"xx"}
LTEemu_SSHInfo={"ip":"10.57.203.4","user":"nokia","password":"nokia123"}
airphone_Asia_SSHInfo={"ip":"167.167.166.61","user":"aa","password":"xx"}
eGate_SSHInfo={"ip":"10.57.203.3","user":"aa","password":"xx"}

LTEemu={"SSHInfo":LTEemu_SSHInfo, "folder":"/home/nokia/LTEemu_V88"}
EPC={"SSHInfo":eGate_SSHInfo, "folder":"/home/nokia/epc_sim_1707"}
UEC={"SSHInfo":eGate_SSHInfo, "folder":"/home/lte/UEC_378"}
RRU={"SSHInfo":gNB_RRU_SSHInfo, "folder":"/ram/hbl"}
FTP={"SSHInfo":ftp_SSHInfo,"folder":"ftp://10.56.6.5/CSV/Testing_Personal/WangJianfeng/Logs/"}

#def init_BB2IP(ip1, ip2, a_or_g):
#    #global airphone_BB2IP
#    BB2Choice=raw_input("""
#if """+a_or_g+""" BB2IP is """+ip1+""", print 1
#if """+a_or_g+""" BB2IP is """+ip2+""", print 2
#if not both, print full IP
#:""")
#    if BB2Choice=="1":
#        return ip1
#    elif BB2Choice=="2":
#        return ip2
#    else:
#        return BB2Choice

#def airphone_BB2_SSHInfo():
#    airphone_BB2IP=init_BB2IP("169.254.228.181","169.254.228.182","airphone")
#    print "your BB2IP is:", airphone_BB2IP
#    airphone_BB2_SSHInfo={"ip":airphone_BB2IP,"user":"_rcpadmin","password":"RCP_owner"}
#    return airphone_BB2_SSHInfo

#def gNB_BB2_SSHInfo():
#    gNB_BB2IP=init_BB2IP("169.254.228.145","169.254.228.146","gNB")
#    print "your gNB BB2IP is:", gNB_BB2IP
#    gNB_BB2_SSHInfo={"ip":gNB_BB2IP,"user":"_rcpadmin","password":"RCP_owner"}
#    return gNB_BB2_SSHInfo

##airphone_BB2_SSHInfo()
##gNB_BB2_SSHInfo()
