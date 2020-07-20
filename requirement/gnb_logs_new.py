#! /bin/python
# 
# This script collects 5G18A cloud gNB logs to local running folder, named as: <GNB_x.x.x.x_YMDHMS.zip>
# It can be run directly on gNB's OAM-0 VM, or from local PC by specifing oam-0 IP address or hostname as below:
#
# ./gnb_logs.py [User@]Host [Password]
#
# 
# Any problem or suggestion, please contact peidong.li@nokia-sbell.com
#
###############################################################

# You can config oam and asik IP here beforehand as well:

oam_ip = ''
rap = ''

###############################################################

#2019.1.25 ver 1.0
version = 1.0


info = """
Usage:
gnb_logs.py [USER@]HOST [PASSWORD] [OPTIONS...]	
      
Options:
  -s, --small        Collect minimum logs only
  -f, --full         Collect full logs
  -t, --tti [time]   Collect ttiTrace for specified seconds
  -r, --rap          Give RAP IP address  
  
  -h, --help         Display this help and exit       

Examples:
  > gnb_logs.py                      ...Collect default logs by run script from GNB's oam-0 
  > gnb_logs.py 10.68.135.99         ...Collect from the addressed GNB, with default robot login
  > gnb_logs.py 10.68.135.99 --full  ...Collect full logs from the GNB
  > gnb_logs.py 10.68.135.99 --rap 192.168.2.60    
                                     ...Give RAP (ASIK) address to save resolving time
  > gnb_logs.py --tti 10             ...Collect ttiTrace log for 10 seconds   
	
	
"""

import paramiko
import time
import sys
import datetime
import logging
import threading
import collections
import os
import re

#Note: make sure the cmd shouldn't contain prompt string...
#remember to always execute 'exit' after login_target() call

#prefix of local log file. 
#full name would be: <prefix + oam ip + time>, like 'GNB_10.56.16.45_20180118_184814.tar.gz'

log_file_prefix = "GNB"
MIN_LOG_SZ = 200


LEVEL_MIN = 1
LEVEL_NORM = 2
LEVEL_FULL = 3

log_level = LEVEL_NORM
local_level = logging.ERROR

#default login info
ssh_port = 22
oam_usr = "robot"
oam_pwd = "rastre1"
oam_prompt = '$ '
oam_max_ses = 10

# to generate several seconds' ttiTrace before collecting, if needed:
TTI_NONE = 0
TTI_INCLUDE = 1
TTI_ONLY = 2

tti_on = TTI_NONE
tti_len = 10
tti_max = 60
tti_path = "/var/ttiTrace/"

owner = {}
#引入字典
hosts = []

MAX_RUNTIME = 300
t_runtime = 0

BAR_LEN = 50
bar_stop = False

class fileException(Exception):
	def __init__(self,info):
		self.info = info
	def __str__(self):
		print self.info
		
def log_setup(my_level):
  # set up logging to file
  logging.basicConfig(level=my_level,
                      format='%(asctime)s %(name)-5s %(levelname)-5s %(message)s',
                      datefmt='%m-%d %H:%M',
                      filename='stdout.log',
                      filemode='w')
  # define a Handler which writes INFO messages or higher to the sys.stderr
  console = logging.StreamHandler()
  console.setLevel(logging.ERROR)
  #console.setLevel(logging.DEBUG)
  # set a format which is simpler for console use
  formatter = logging.Formatter('%(name)-5s: %(levelname)-5s %(message)s')
  # tell the handler to use this format
  console.setFormatter(formatter)
  # add the handler to the root logger
  logging.getLogger('').addHandler(console)

def send_str_and_wait(shell, log_header, command, wait_time):
	logging.debug ("_" + log_header + " [s::" + command + "]+")
	shell.send(command)
	buff = ""
	time.sleep(wait_time)
	buff = shell.recv(8192)
	logging.debug ("_" + log_header + " [r::" + buff+"].")
	return buff
	
def send_str_wait_str(shell, log_header, command, wait_str, escapes=None, response=None, enter=True, rcv_key=None,tot_key=None,callback=None):
	r = 0
	i = 0
	#enter是用于检测指令是否敲回车了
	if enter:
		if not str(command).endswith('\n'):
			command += '\n'
	shell.send(command)
	logging.debug ("_"+log_header + " [s:"+command+"]"+wait_str)
	rcv_buf = ''
	#while not wait_str in rcv_buf:
	#当没有以$结尾时，也就是说，当ssh出现验证问题时 or执行指令出现问题时(obsolete)
	#因为每次进这个函数，都先让rcv_buf = ''，也就是把buffer的东西清空，这样每次调用此函数，一定会走进下面的while not里面
	while not rcv_buf.endswith(wait_str):
		if shell.recv_ready():
			#recv_ready()是paramiko里面的东西，因为shell 是上一个函数start_ses里面带的paramiko.SSHClient.invoke_shell
			#但是recv_rady是paramiko.channel里面的东西，难怪那个带入的参数缩写是ch
			#channel 的buffer里只要有东西，这个就会是true
			rcv_buf += shell.recv(9000)
			#这个是shell.recv是表示去从channel的buffer里面去读，最多可以收9000
			logging.debug ("_"+log_header + " [r:"+rcv_buf+"]")
			if rcv_key:
				n = rcv_buf.count(rcv_key)
				if n:
					if callback:
						callback(n,tot_key)
			if response:
			#这里response为真，但是现在还不明白为啥把enter设为false，这里就进不去最里层了（obsolete)
            #这个if enter只是为了判断有没有敲回车，shell.send(response[key])是跟他平行的，别看错了，
				for key in response:
					if key in rcv_buf:
						if enter:
							response[key]+='\n'
						shell.send(response[key])
						#time.sleep(2)
						logging.debug ("_"+log_header + " [s:"+ response[key] + "]")
						rcv_buf = ''
						break
			if escapes:
			#这里只是打印下错误的log
				for elem in escapes:
					if elem in rcv_buf:
						logging.error("_" + log_header + " rcv fail:" + elem + " !")
						r = 1
						return (r, rcv_buf)
	logging.info("_" + log_header + " " + rcv_buf)
	return (r, rcv_buf)

def get_jour_log(shell, node_name, shell_prompt):
	files = 0
	ssh = ''
	if '$' in shell_prompt:
		ssh = 'sudo '
	#ssh += "journalctl -b | gzip> /tmp/"+(node_name)+"_journal_log.gz\n"
	ssh += "journalctl -b > /tmp/"+(node_name)+"_journal.log\n"
	ret,buf = send_str_wait_str(shell, node_name, ssh, shell_prompt)
	if not ret:
		files+=1

	return files
	
def get_aashell_logs(shell, node_name, shell_prompt):
	files=0
	esp = ['timed out','Connection refused',shell_prompt] #'Connection closed'
	rsp = {'telnet>':'quit\n','exit telnet':'e\n','^]':'\n'}
	buf = send_str_and_wait(shell, node_name, "telnet 0 15007\n", 6)
	if not "AaShell>" in buf:
		if not shell_prompt in buf:
			send_str_wait_str(shell, node_name, "\x1D", shell_prompt,esp,rsp,False)
		logging.error("_" + node_name + " collect AaShell logs failed!")
	else:
		send_str_wait_str(shell, node_name, "log -c full -z "+node_name+"_aashell_log.zip\n", "AaShell> ",esp)
		send_str_wait_str(shell, node_name, "quit\n", shell_prompt,esp)    
		files +=1
	return files
		
def get_res_log(shell, node_name, shell_prompt):
	files = 0

	send_str_wait_str(shell, node_name, "echo -e '\n\n###date;uptime'>> /tmp/"+(node_name)+"_stat.log\n", shell_prompt)
	send_str_wait_str(shell, node_name, "date>> /tmp/"+(node_name)+"_stat.log\n", shell_prompt)
	send_str_wait_str(shell, node_name, "uptime>> /tmp/"+(node_name)+"_stat.log\n", shell_prompt)
	send_str_wait_str(shell, node_name, "echo -e '\n\n###top -n 2'>> /tmp/"+(node_name)+"_stat.log\n", shell_prompt)
	send_str_wait_str(shell, node_name, "top -b -n 1 -w>> /tmp/"+(node_name)+"_stat.log\n", shell_prompt)
	send_str_wait_str(shell, node_name, "echo -e '\n\n###df -h'>> /tmp/"+(node_name)+"_stat.log\n", shell_prompt)
	send_str_wait_str(shell, node_name, "df -h>> /tmp/"+(node_name)+"_stat.log\n", shell_prompt)
	send_str_wait_str(shell, node_name, "echo -e '\n\n###ifconfig'>> /tmp/"+(node_name)+"_stat.log\n", shell_prompt)	
	send_str_wait_str(shell, node_name, "ifconfig>> /tmp/"+(node_name)+"_stat.log\n", shell_prompt)
	files +=1
	
	return files

def scp_log(shell, node_name, shell_prompt, sftp_ip, sftp_usr, sftp_pwd): 
	esp = ['timed out','Connection refused','Permission denied']
	rsp = {'? (y/n)':'y','?':'yes','assword:':sftp_pwd}
	ssh = "scp /tmp/"+(node_name)+"_* "+sftp_usr+"@"+sftp_ip+":/tmp"
	
	ret,buf = send_str_wait_str(shell, node_name, ssh, shell_prompt, esp, rsp)
	if ret:
		logging.info("_" + node_name + " scp file transfer failed!")
	
	#cleanup
	send_str_wait_str(shell, node_name, "rm -f /tmp/" + node_name + "_*", shell_prompt)	  

def scp_log2(shell, node_name, shell_prompt, fname, d_folder, sftp_ip, sftp_usr, sftp_pwd):
	  #time.sleep(1)
	  buf = send_str_and_wait(shell, node_name, "scp " + fname + " " + sftp_usr + "@"+sftp_ip+":" + d_folder + "\n", 4)
	  if "?" in buf:
	  	send_str_and_wait(shell, node_name, "yes\n",2)
	  ret,buf1 = send_str_wait_str(shell, node_name, sftp_pwd+"\n", shell_prompt)
	  #cleanup
	  send_str_wait_str(shell, node_name, "rm -f " + fname + "\n", shell_prompt)	  

def scp_from(shell, node_name, shell_prompt, fname, d_folder, sftp_ip, sftp_usr, sftp_pwd):
	  buf = send_str_and_wait(shell, node_name, "scp " + sftp_usr + "@"+sftp_ip+":" + fname + " " + d_folder + "\n", 4)
	  if "?" in buf:
	  	send_str_and_wait(shell, node_name, "yes\n",2)
	  ret,buf1 = send_str_wait_str(shell, node_name, sftp_pwd+"\n", shell_prompt)
	
def tti_bar(sec):
	global bar_stop
	sys.stdout.flush() 
	i =0
	p =0
	sleep = 1
	while (not bar_stop) and (p<BAR_LEN):
		
		if i*sleep <= sec:
			p = int(BAR_LEN*(i*sleep)/sec)
		ProgressBar("\r[{}] {:.0f}% {}", p)
		logging.debug('tti refresh:'+datetime.datetime.now().ctime()+',p='+str(p)+', sec='+str(sec))
		time.sleep(sleep)
		sys.stdout.flush() 
		i+=1
		
def unzip_cb(kws,tot_kws):
	i = (BAR_LEN-10)*kws/tot_kws
	if i < BAR_LEN -10:
		ProgressBar("\r[{}] {:.0f}% {}", i, BAR_LEN-10, BAR_LEN-10)

def decode_cb(kws,tot_kws):
	i = (BAR_LEN)*kws/tot_kws
	if i < BAR_LEN:
		ProgressBar("\r[{}] {:.0f}% {}", i, BAR_LEN, BAR_LEN)
		
def tti_gen(s_node,d_node):
	if not login_target(s_node, d_node):
		global bar_stop
		bar_stop = False
	
		#try:
		sys.stdout.write('Generating TTI trace ('+str(tti_len)+'s)...\n')
		t = threading.Thread(target=tti_bar, args=(tti_len,))
		t.setDaemon(True)
		t.start()
		send_str_wait_str(s_node['chan'], d_node['name'],'rm -f ' + tti_path + '*',d_node['prompt'])
		send_str_and_wait(s_node['chan'], d_node['name'], "/opt/tools/ttiTrace/collect.sh\n", 1)
		time.sleep(tti_len)
		bar_stop = True

		iret, buf = send_str_wait_str(s_node['chan'],d_node['name'],'\x03',d_node['prompt'])
		iret, buf = send_str_wait_str(s_node['chan'],d_node['name'],'\x03',d_node['prompt'])

		#read two more lines
		send_str_and_wait(s_node['chan'],d_node['name'],'\n',2)

		#send_str_wait_str(s_node['chan'],d_node['name'],'',d_node['prompt'],None,None)
		#send_str_wait_str(s_node['chan'],d_node['name'],'',d_node['prompt'],None,None)
		
		send_str_wait_str(s_node['chan'], d_node['name'], "cd " + tti_path + "\n", d_node['prompt'])
		sys.stdout.write('Processing...\n') 
		ret, buf = send_str_wait_str(s_node['chan'],d_node['name'],'ls *.gz -l',d_node['prompt'])
		num = re.findall('\s5GTtiTrace\.bin\.\d+\.tar.gz',buf)
		logging.info('tti tar.gz: '+ str(len(num)))
		if len(num) ==0:
			logging.error('No ttiTrace file generated!')
			end_login_target(s_node, d_node, s_node['prompt'])
			return 1
						
		#todo: bar
		send_str_wait_str(s_node['chan'], d_node['name'], "ls *.tar.gz | xargs -n1 tar xzvf", d_node['prompt'],None,None,True,'5GTtiTrace.bin.',len(num),unzip_cb)
		#lpdt
#			iret, buf=send_str_wait_str(s_node['chan'], d_node['name'], 'for file in /var/ttiTrace/*.bin.*; do /opt/tools/ttiTrace/TtiTraceDecoder "$file" "$file" ;done', d_node['prompt'],None,None,True,'Ring Buffer Header',len(num))			
		
		send_str_wait_str(s_node['chan'], d_node['name'], "rm *.tar.gz", d_node['prompt'])	
		iret, buf=	send_str_wait_str(s_node['chan'], d_node['name'], "ls -l", d_node['prompt'])	
		num = re.findall('\s5GTtiTrace\.bin\.\d',buf)
		logging.info('tti .bin: '+ str(len(num)))
		if len(num) ==0:
			logging.error('No ttiTrace file unzipped!')
			logging.info(num)
			bar_stop = True
			end_login_target(s_node, d_node, s_node['prompt'])
			return 1

		print '\nDecoding...\n'			
		iret, buf=send_str_wait_str(s_node['chan'], d_node['name'], 'for file in /var/ttiTrace/*.bin.*; do /opt/tools/ttiTrace/TtiTraceDecoder "$file" "$file" ;done', d_node['prompt'],None,None,True,'Ring Buffer Header',len(num),decode_cb)

		iret, buf =	send_str_wait_str(s_node['chan'], d_node['name'], "ls -l *.csv", d_node['prompt'])	
		files = re.findall('\s5GTtiTrace\.bin\.\d+\..l.csv',buf)
		logging.debug('tti csv:' + str(len(files)))
		if len(files) < 1:
			if '-bash: fork' in buf:
				print '\nError: '+buf
			logging.error('No ttiTrace file decoded!')
			end_login_target(s_node, d_node, s_node['prompt'])
			return 2
				
		send_str_wait_str(s_node['chan'], d_node['name'], 'tar zcvf /tmp/'+d_node['name']+'_ttiTrace.tar.gz *.csv', d_node['prompt'])
		send_str_wait_str(s_node['chan'], d_node['name'], 'rm *', d_node['prompt'])
		
		d_node['files']+=1
		if d_node['files']:
			if d_node.has_key('routr'):
				scp_log(s_node['chan'], d_node['name'], d_node['prompt'], d_node['routr']['rip'], d_node['routr']['usr'], d_node['routr']['pwd'])
				send_str_and_wait(s_node['chan'], d_node['name'], "exit\n", 2)
				scp_log(s_node['chan'], d_node['name'], d_node['routr']['prompt'], d_node['routr']['om'], oam_usr, oam_pwd)		
		end_login_target(s_node, d_node, s_node['prompt'],True)

	#	except Exception as e:
	#		print 'Exception:'
	#		print(e)
	#		logging.error('Exception got')
	#		end_login_target(s_node, d_node, s_node['prompt'])
	#		bar_stop =True
		
	else:
		logging.error('Login '+ d_node['name'] + ' failed!')
		return 1
	return 0

def bb2_misc_logs(node):
	sh = '/opt/tools/checkCellSetup/checkCellSetup.sh>> /tmp/' + node['name'] +  '_cellsetup.log'
	send_str_wait_str(node['chan'], node['name'], sh, node['prompt'])
	sh = 'cp /ffs/run/swconfig.txt '+'/tmp/'+node['name']+'_swconfig.txt'
	send_str_wait_str(node['chan'], node['name'], sh, node['prompt'])
	sh = "for f in startup_*; do cp $f " + node['name'] + "_$f; done\n"
	#这些shell指令最好在环境上敲一下，是什么返回
	send_str_wait_str(node['chan'], node['name'], 'cd /tmp', node['prompt'])
	send_str_wait_str(node['chan'], node['name'], sh, node['prompt'])
	node['files'] += 1

def asik_misc_logs(node):
	sh = 'cp /ffs/run/swconfig.txt '+'/tmp/'+node['name']+'_swconfig.txt'
	send_str_wait_str(node['chan'], node['name'], sh, node['prompt'])
	sh = "for f in startup_*; do cp $f " + node['name'] + "_$f; done\n"
	send_str_wait_str(node['chan'], node['name'], 'cd /tmp', node['prompt'])
	send_str_wait_str(node['chan'], node['name'], sh, node['prompt'])
	node['files'] += 1

def ru_misc_logs(node):
	send_str_wait_str(node['chan'], node['name'], sh, node['prompt'])
	sh = "cp /ram/startup_DEFAULT.log.xz /tmp/" + node['name'] +"_startup_DEFAULT.log.xz"
	send_str_wait_str(node['chan'], node['name'], sh, node['prompt'])
	sh = "cp /ram/startup_DEFAULT.log /tmp/" + node['name'] +"_startup_DEFAULT.log"
	send_str_wait_str(node['chan'], node['name'], sh, node['prompt'])
	node['files'] += 1
		

def start_ses():
		s = paramiko.SSHClient()
		s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		s.connect(oam_ip,ssh_port,oam_usr,oam_pwd)
		ch = s.invoke_shell()
		esp = ['login denied']
		rsp = {'?':'yes','assword:':oam_pwd}
		ret,buf = send_str_wait_str(ch,'OAM','',oam_prompt,esp,rsp,False)
	    #此处引入交互式的字符发送和等待，这个send_str_wait_str以后可以很大程度上在别的脚本里复用！！take care
		if ret:
			logging.fatal ("_OAM: cannot login OAM!")
		return ret, s, ch
		#返回一个channel用于shell使用，返回一个s用于SSH使用，返回ret是result，看看登陆是否成功，成功就为0

def close_ses(node):
	if node.has_key('routr'):
		send_str_and_wait(node['chan'], node['name'], "exit\n", 2)
	send_str_and_wait(node['chan'], node['name'], "exit\n", 2)
	node['conn'].close()	
	logging.info( "_" + node['name'] + " thread exiting")

#visit d_node from s_node session. s==d if thread create up.
#remember pair use with end_login_target() if not thread
#也就是说 从s_node ssh 到d_node. 如果多线程的话，s==d
def login_target(s_node,d_node,skip_routr=False,p_node=None):
	routr_ok = False
	result = 0
	if s_node == d_node and p_node:
		n = p_node
	else:
		n = s_node	
		#n=oam
	esp = []  #'timed out','Permission denied','Too many Password failures',,'Connection refused'
	if not skip_routr and d_node.has_key('routr'):
	#这里的d_node是刚刚里面的DU，里面没有定义routr，所以这里走不进去
		if not n['prompt'] == d_node['routr']['prompt']:
			if not n['prompt'] == d_node['prompt']:
				esp.append(n['prompt'])
			else:
				esp.append(n['prompt_kw'])
		rsp = {'?':'yes','assword:':d_node['routr']['pwd']} #'denied, please try again':'\x03'
		ssh = "ssh "+ d_node['routr']['usr'] + "@" + d_node['routr']['ip']
		if d_node['routr'].has_key('opt'):
			ssh += d_node['routr']['opt']
		ret,buf = send_str_wait_str(s_node['chan'], s_node['name'], ssh, d_node['routr']['prompt'], esp, rsp)
		if ret:
			logging.error("_" + s_node['name'] + " Login " + d_node['routr']['name'] + " failed!")
			return -1
		routr_ok = True
		
	ssh = 'ssh '+ d_node['usr'] + '@'+ d_node['ip']
	#这里的ip是du的ip ssh toor4nsn@rap
	if d_node.has_key('opt'):
		ssh += d_node['opt']
		#用复杂的ssh -o等参数的方式登陆
	if routr_ok:
	#默认false，走不进这里，先不看2.1
		if not d_node['routr']['prompt'] == d_node['prompt']:
			esp.append(d_node['routr']['prompt'])
	elif not d_node['prompt'] == n['prompt']:
	#这里的n是s_node，也就是get_cu里面带的owner，那么owner的prompt是$，跟d_node里面的>是不一样的，所以走进这个elif not
		esp.append(n['prompt'])
		#append '>'
	rsp = {'?':'yes','assword:':d_node['pwd']} #,'denied, please try again':'\x03'
	ret,buf = send_str_wait_str(s_node['chan'], s_node['name'], ssh, d_node['prompt'], esp, rsp)
	#试图从channel的shell里ssh到DU，但是现在应该是在oam上吧，因为s_node是oam

	logging.debug('login:'+str(ret) + ', s,d, p:'+ s_node['name'] +','+d_node['name'] + ', '+n['name'] +'  esp:' + ''.join(esp) )
    #ret应该是result的意思，也就是result好的话，那么result为0
	if ret:
	#ret正常情况下也是0，所以不走进此if
		result = 2
	if d_node.has_key('prompt_kw') and not d_node['prompt_kw'] in buf:
		#du的prompt_kw是@fct, buf的prompt_kw是看登进去没，如果登进去了，那就是一样的，
		#所以正常情况下，不走进这个if
		result = 3
	if result:
	#正常不走进此if
		logging.error("_" + s_node['name'] + " Login " + d_node['name'] + " failed!")
		if routr_ok and d_node['routr']['prompt_kw'] in buf:
			send_str_wait_str(s_node['chan'], s_node['name'], 'exit', s_node['prompt'])
	return result
	#正常result是0

def end_login_target(s_node,d_node,prompt,skip_routr=False):
	if not skip_routr:
	#一般不会填这个，所以要走进来这个if not
		if d_node.has_key('routr'):
		#du没有这个routr
			send_str_wait_str(s_node['chan'], s_node['name'], 'exit', d_node['routr']['prompt'])
	send_str_wait_str(s_node['chan'], s_node['name'], 'exit\n', prompt)
				
def log_r(node, nodes):		

	if node.has_key('pre'):
		node['pre'](node)
		node['bar_i'] = BAR_LEN / 5
	
	node['files'] += get_res_log(node['chan'], node['name'], node['prompt'])
	node['bar_i'] = BAR_LEN / 4

	node['files'] += get_jour_log(node['chan'], node['name'], node['prompt'])
	node['bar_i'] = BAR_LEN /2
	
	if log_level == LEVEL_FULL:
		node['files'] += get_aashell_logs(node['chan'], node['name'], node['prompt'])
		node['bar_i'] = BAR_LEN *3 / 4
		
	if node['files']:
		if node.has_key('routr'):
			scp_log(node['chan'], node['name'], node['prompt'], node['routr']['rip'], node['routr']['usr'], node['routr']['pwd'])
			node['bar_i'] = BAR_LEN *4/5
			send_str_and_wait(node['chan'], node['name'], "exit\n", 2)
			scp_log(node['chan'], node['name'], node['routr']['prompt'], node['routr']['om'], oam_usr, oam_pwd)
			node['bar_i'] = BAR_LEN
		else:
			if(node['name'] != "oam-0.local"): #skip oam				
				scp_log(node['chan'], node['name'], node['prompt'], node['om'], oam_usr, oam_pwd) 
				node['bar_i'] = BAR_LEN
	close_ses(node)
	node['bar_i'] = BAR_LEN

def all_nodes_fnames(nodes):
		names = ""
		for i in range(0, len(hosts)):
			if nodes[i]:
				names += nodes[i]['name'] + "_* "
		return names
		
def router_fnames(node,nodes):		 #??
	#host是一个全球变量，所以取log的思路是先去CU里面，存一堆VM的名字到host里面，然后一个个去登陆，取log
	#再clear，然后把DU里面的各个abil的main和subordinate存到host里面，然后一个个登陆并去取log
	names = node['name'] + "_* "
	for i in range(0, len(hosts)):
		if nodes[i]:
		#当hosts里面还有东西时
			if nodes[i].has_key('routr'):
			#DU的host里面才有routr这种参数
				if nodes[i]['routr']['ip'] == node['ip']:
					names += nodes[i]['name'] + "*_ "
	return names
								
def clean_up(node, all_files=0, nodes=None): 
	send_str_wait_str(node['chan'], node['name'], "cd /tmp\n", node['prompt'])
	names = node['name'] + "_*"
	#names = OAM-0_*
	if not all_files:
	#clean的时候是1，所以不走进这个if not,进else
	#bat_log里面这里是0，所以要进
		if nodes is not None:
		#这里指nodes里面，也就是hosts里面还有没有没登陆的host，如果有就走进来，
			names = router_fnames(node,nodes)
			#返回host里面有routr的names，都变成name*_
	else:
		if nodes is not None:
			names = all_nodes_fnames(nodes)
			#返回所有host里面的names，都变成name_*
	sh = ''
	if '$ ' in node['prompt']:
		sh += 'sudo '
	sh += 'rm -f ' + names
	#sudo rm -f OAM_*
	#sudo rm -f name*_是删的啥子东西？？？去了公司一定要试下这段指令
	#这里为什么会用shell去删除这些host，难道在哪儿保存了下来？？
	send_str_wait_str(node['chan'], node['name'], sh, node['prompt'])
	
def sftp_cb(bytes,tot_bytes):
	i = (BAR_LEN+10)*bytes/tot_bytes
	ProgressBar("\r[{}] {:.0f}% {}", i, BAR_LEN+10, BAR_LEN+10)
	
def log_download(node, nodes):
	names = all_nodes_fnames(nodes)
	fname = log_file_prefix + "_"+ oam_ip + "_" + time.strftime('%Y%m%d_%H%M%S',time.localtime(time.time())) #+ ".tar.gz"
	##may rcv too early and leave ram] part soon for next routine if it's not included here:
	send_str_wait_str(node['chan'], node['name'], "cd ~\n", node['prompt'])
	send_str_wait_str(node['chan'], node['name'], "cd /tmp\n", "tmp]\r\r\n" + node['prompt'])
	send_str_wait_str(node['chan'], node['name'], "mkdir "+ fname, node['prompt'])
	send_str_wait_str(node['chan'], node['name'], "mv "+ names + fname, node['prompt'])
	if not tti_on ==TTI_ONLY:		
		send_str_wait_str(node['chan'], node['name'], "cd "+ fname, node['prompt'])
		if not log_level == LEVEL_MIN :
			send_str_wait_str(node['chan'], node['name'], "mkdir sw", node['prompt'])
			send_str_wait_str(node['chan'], node['name'], "mv *swconfig.txt ./sw/", node['prompt'])
			send_str_wait_str(node['chan'], node['name'], "mkdir usage", node['prompt'])
			send_str_wait_str(node['chan'], node['name'], "mv *_stat.log ./usage/", node['prompt'])
			send_str_wait_str(node['chan'], node['name'], "mkdir startup", node['prompt'])
			send_str_wait_str(node['chan'], node['name'], "mv *startup* ./startup/", node['prompt'])
			send_str_wait_str(node['chan'], node['name'], "mv *cellsetup.log ./startup/", node['prompt'])
			#todo:
			#send_str_wait_str(node['chan'], node['name'], "mv "+, node['prompt'])
		send_str_wait_str(node['chan'], node['name'], "cd ..", node['prompt'])
		
	send_str_wait_str(node['chan'], node['name'], "zip -r "+ fname + ".zip " + fname, node['prompt'])	

	ret,buf = send_str_wait_str(node['chan'], node['name'], "ls -l "+ fname + ".zip |awk '{print $5}'\n", node['prompt'])	
	sz = re.findall(r"\r\n(\d+)\r\n", buf, re.S)
	if not len(sz) or ( len(sz) and (int(sz[0]) < MIN_LOG_SZ) ):
		send_str_wait_str(node['chan'], node['name'], "rm -rf " + fname + "*\n", node['prompt'])
		logging.error("Failure in tar, no file downloaded!")		
		return 1
	#send_str_wait_str(node['chan'], node['name'], "rm -f " + fname +"*", node['prompt'])
	
	print '\nStart log downloading...\n'
	sftp = node['conn'].open_sftp()
	sftp.get('/tmp/'+fname+'.zip', fname+'.zip',sftp_cb)
	if  file_exist(fname+'.zip'):
		send_str_wait_str(node['chan'], node['name'], "rm -rf " + fname + "\n", node['prompt'])
		if not os.path.abspath('.')=='/tmp':
			send_str_wait_str(node['chan'], node['name'], "rm -f " + fname + ".zip\n", node['prompt'])
		logging.info ( fname + " is downloaded")
		if os.name == 'nt':
			char = "\\"
		else:
			char = "/"
		print '\nLog file: \n'+os.path.abspath('.')+char+fname+'.zip'
	else:
		logging.error("failed in sftp download!")
		sftp.close()
		return 2
	sftp.close()
	return 0

def file_exist(fname):
	return  os.path.exists(fname) and os.path.isfile(fname) and os.access(fname, os.R_OK)

def upload_file(node,d_node,fname,d_folder,in_d_node):
	sftp = node['conn'].open_sftp()
	if d_node == node:
		sftp.put(fname, os.path.join(d_folder, fname))
		sftp.close()
		return
	res = sftp.put(fname, os.path.join("/tmp/", fname))
	if in_d_node:
		#scp_from(shell, node_name, shell_prompt, fname, d_folder, sftp_ip, sftp_usr, sftp_pwd):
		scp_from(node['chan'], node['name'], d_node['prompt'], "/tmp/"+fname, d_folder, d_node['om'], oam_usr, oam_pwd)
	else:
		scp_log2(node['chan'], node['name'], node['prompt'], "/tmp/"+fname, d_folder, d_node['ip'], d_node['usr'], d_node['pwd'])
	sftp.close()

def get_ip(node, *ifs):
	dic=[]
	if node is None:
		output = os.popen('ip a')
		buf = output.read()
	else:
		ret,buf = send_str_wait_str(node['chan'], node['name'], "ip a\n", node['prompt'])
	for i,ifc in enumerate(ifs):
		exp = '\s'+ ifc + ':\s[\s\S]+?inet\s((?:[0-9]{1,3}\.){3}[0-9]{1,3})'
		ip = re.findall(exp,buf)
		if ip:
			dic.append({'ifc':ifc,'ip':''.join(ip)})
	if dic is None:
		return None
	return dic
	
def get_if(ch,name,prompt,ifc):
	if ch is None:
		output = os.popen('ip a sh dev ' + ifc)
		#ip a指令，再用dev去指定具体端口
		#ps，popen是一个已经被嫌弃的函数，大都被替换成subprocess,详情参考如下链接(后续自己试着换一下)
		#https://docs.python.org/2/library/subprocess.html#replacing-os-popen-os-popen2-os-popen3
		buf = output.read()
		#os.read() 配合os.open or os.popen 来读出刚刚获得的interface的详细信息，然后在下面的ip处用正则表达式去提取出ip
	else:
		ret,buf = send_str_wait_str(ch, name, 'ip a sh dev '+ifc+'\n', prompt)
	ip = re.findall('inet\s((?:[0-9]{1,3}\.){3}[0-9]{1,3})',buf)
	#正则表达式提取出ip
	#匹配到inet这排，然后\s表示匹配任意空白字符（包括空白，制表符，换页等）
	#第一个括号里面, (?:pattern)表示匹配pattern，但不获取结果。
	#[0-9]表示匹配0-9中任意一个数
	#{1-3}表示匹配1-3次
	#\.  本来.是要匹配除了换行符的任何字符，加上\之后，应该是让他只匹配.本身
	#括号外面的{3}是要确定匹配三次（因为正常的ip都是4端，前三段都包括xxx. 而第四段只有xxx 
	#所以第4段单独列出来匹配，所以完成了整个ip的匹配
	if ip:
		if len(ip) > 1:
			return ''.join(ip[0])
		else:
			return ''.join(ip)
	return ''

def get_cur_ses(s_node):
	r,buf = send_str_wait_str(s_node['chan'],s_node['name'],'who',s_node['prompt'])
	#执行who的时候返回who 命令显示关于当前在本地系统上的所有用户的信息
	s = re.findall('(.+\(((?:[0-9]{1,3}\.){3}[0-9]{1,3})\))',buf)
	#.匹配任意的字符 
	#+匹配前面的子表达式一次或多次
	#后面是获取IP
	return len(s)

def pending_bar(i):
	global bar_stop
	sys.stdout.flush() 								
	while not bar_stop:
		if (i%4) == 0: 
		    sys.stdout.write('\b/')
		elif (i%4) == 1: 
		    sys.stdout.write('\b-')
		elif (i%4) == 2: 
		    sys.stdout.write('\b\\')
		elif (i%4) == 3: 
		    sys.stdout.write('\b|')		
		sys.stdout.flush()
		time.sleep(0.2)
		i+=1	
	print '\b\b\b'
	
def get_cu_hosts(s_node, du_ip=None):
	#这里的s_node是CU，那也就是说，去DU是从CU ssh过去的
	#这个函数的主要内容是获取CU的各个VM的名字，写好字典，并放进hosts这个list
	#最后会尝试进入DU，然后获得rlan0的IP，为什么要获得rlan0的ip，是为了进abil？？
	global bar_stop
	if du_ip:
		buf = 'cpcl-0.local,cpif-0.local,cpue-0.local,upue-0.local,cpnb-0.local,db-0.local'
		addr = [du_ip]
	else:
	#暂时不看else，反正填了rap IP的话，不走这里
		bar_stop = False
		try:
			#send_str_wait_str(s_node['chan'],s_node['name'],"echo '  wait 2+ minutes for data retrieving......'",s_node['prompt'])
			sys.stdout.write('Retrieving data, takes 1 minute or more...    ')
			t = threading.Thread(target=pending_bar, args=(2,))
			t.setDaemon(True)
			t.start()
			ret,buf = send_str_wait_str(s_node['chan'],s_node['name'],'arp -a\n',s_node['prompt'])
			ip = re.findall('\(((?:[0-9]{1,3}\.){3}[0-9]{1,3})\)\sat\s(.+)\s\[.+\]\s{2}on\sfronthaul',buf)
			addr=[]
			mac=[]
			for val in ip:
				if val[1] not in mac:
					mac.append(val[1])
					if cmp(val[0],owner['internal']):
						addr.append(val[0])		
		except Exception as e:
			bar_stop = True
			print(e)
		bar_stop = True
	
	
	if 'cpcl-0.local' in buf:
		h={}
		h['name'] = 'cpcl-0'
		h['ip'] = 'cpcl-0.local'
		h['usr'] = oam_usr
		h['pwd'] = oam_pwd
		h['om'] = 'oam-0.local'
		h['prompt'] = '$ '
		h['prompt_kw'] = h['name']
		hosts.append(h)
	if 'cpif-0.local' in buf:
		h={}		
		h['name'] = 'cpif-0'
		h['ip'] = 'cpif-0.local'
		h['usr'] = oam_usr
		h['pwd'] = oam_pwd
		h['om'] = 'oam-0.local'
		h['prompt'] = '$ '
		h['prompt_kw'] = h['name']
		hosts.append(h)		
	if 'cpue-0.local' in buf:
		h={}		
		h['name'] = 'cpue-0'
		h['ip'] = 'cpue-0.local'
		h['usr'] = oam_usr
		h['pwd'] = oam_pwd
		h['om'] = 'oam-0.local'
		h['prompt'] = '$ '
		h['prompt_kw'] = h['name']
		hosts.append(h)		
	#consider multi vm later...
	if 'upue-0.local' in buf:
		h={}		
		h['name'] = 'upue-0'
		h['ip'] = 'upue-0.local'
		h['usr'] = oam_usr
		h['pwd'] = oam_pwd
		h['om'] = 'oam-0.local'
		h['prompt'] = '$ '
		h['prompt_kw'] = h['name']
		hosts.append(h)		
	if 'cpnb-0.local' in buf:
		h={}		
		h['name'] = 'cpnb-0'
		h['ip'] = 'cpnb-0.local'
		h['usr'] = oam_usr
		h['pwd'] = oam_pwd
		h['om'] = 'oam-0.local'
		h['prompt'] = '$ '
		h['prompt_kw'] = h['name']
		hosts.append(h)	
	if 'db-0.local' in buf:
		h={}		
		h['name'] = 'db-0'
		h['ip'] = 'db-0.local'
		h['usr'] = oam_usr
		h['pwd'] = oam_pwd
		h['om'] = owner['internal']
		h['prompt'] = '$ '
		h['prompt_kw'] = h['name']
		hosts.append(h)		
		
	logging.debug(addr)
	i=0		
	for k in addr:
			h={}
			h['pre_name'] = ''
			if len(addr) > 1:
				h['pre_name'] =  'rap-' + str(i) + '-'
			h['name'] = h['pre_name'] + 'fctla'
			h['ip'] = ''.join(k)
			h['opt'] = ' -o BatchMode=no -o PasswordAuthentication=yes -o PreferredAuthentications=password'
			h['usr'] = "toor4nsn"
			h['pwd'] = "oZPS0POrRieRtu"
			h['om'] = owner['internal']
			h['prompt'] = " >"
			h['prompt_kw'] = '@fct'
			if not login_target(s_node, h):
			#这里的s_node是oam
			#正常情况下lonin_target是回0的，所以正常是要走进这个if not的
				h['rip'] = get_if(s_node['chan'],s_node['name'],h['prompt'],'rlan0')
				#也就是说已经进去到DU了，然后要获取rlan0的IP
				if h['rip']:
					hosts.append(h)
					i+=1
				end_login_target(s_node,h,s_node['prompt'])
				#这个函数貌似是为了退出来(执行exit指令)
			else:
				#h['rip'] = 'fct'
				continue

def get_du_hosts(s_node,d_node):		
	if login_target(s_node, d_node):
		return
	ret,buf = send_str_wait_str(s_node['chan'],s_node['name'],'arp -a\n',d_node['prompt'])
	if 'fctlb' in buf:
		h={}		
		h['name'] = d_node['pre_name']+'fctlb'
		h['ip'] = 'fctlb'
		h['usr'] = 'toor4nsn'
		h['pwd'] = 'oZPS0POrRieRtu'
		h['routr'] = d_node 
		h['prompt'] = ' >'
		h['prompt_kw'] = 'b:'
		hosts.append(h)	
	ip = re.findall('(fsp-\d-\d.)\s\(\d',buf) 
	#\d匹配一个数字字符0-9，.匹配单个字符，\s匹配空白字符
	#这儿最好结合环境一起看，大意反正是获取DU和RU的一些host
	if ip:
		ip = {}.fromkeys(ip).keys()  #remove duplication
		for i,val in enumerate(ip):
			h={}		
			h['name'] = d_node['pre_name'] + val
			h['ip'] = val
			h['usr'] = 'toor4nsn'
			h['pwd'] = 'oZPS0POrRieRtu'
			h['routr'] = d_node 
			if val.endswith('c'):  #fsp-x-xc
				h['prompt'] = '# '
			else:
				h['prompt'] = ' >'
			h['prompt_kw'] = 'aspa-'
			hosts.append(h)
			#ru
			if val.endswith('c'):
				if not login_target(s_node, h, True):
					ret2, buf2 = send_str_wait_str(s_node['chan'],s_node['name'],'ip neigh',h['prompt'])
					ip2 = re.findall('((?:[0-9]{1,3}\.){3}[0-9]{1,3})\sdev\seth1',buf2)
					for k in ip2:
						h={}
						h['name'] = d_node['pre_name'] + 'ru'
						h['ip'] = ''.join(k)
						h['usr'] = "root"
						h['pwd'] = "umniedziala"
						h['routr'] = d_node 
						h['prompt'] = "$ "	
						h['prompt_kw'] = '(hw-'	
						hosts.append(h)
						break
					end_login_target(s_node,h,d_node['prompt'],True)
	end_login_target(s_node, d_node, s_node['prompt'])

def add_rap_rout(s_node,d_node):
	if not login_target(s_node, d_node):
		send_str_wait_str(s_node['chan'],s_node['name'],'ip r ad '+owner['internal']+' via '+owner['fronthaul']+' dev fp0\n',d_node['prompt'])
		end_login_target(s_node, d_node, s_node['prompt'])

def run_log_r():
	#没看懂这个函数想干嘛，开多线程？
	global hosts
	ses = oam_max_ses - get_cur_ses(owner) -1
	#oam_max_ses =10这个10它是怎么得来的，这个ses是指的session
	if ses <= 0:
		logging.fatal('Too many open sessions, no possible for logs!')
		ses = 0
		return 0
	logging.info("max ses: "+str(ses) + 'for:'+str(len(hosts)))
		
	n = len(hosts)
	i = 0
	j = 0
	while n and ses>0:
		logging.debug('n,i,j:'+str(n)+','+str(i)+','+str(j))
		if n > ses:
			j += ses
			#j = j+ses=ses
			bat_logs(i,j-1)
			#bat_logs(0,ses-1)
			i = j
			#i=ses
			n -= ses
			#n=n-ses
			continue
		else:
			bat_logs(i,j+n-1)
			n = 0
				
	logging.info("log_r totally done. ")
	return len(hosts)
						
def handle_argvs():
	#handle_argvs 里的sys.argv 是用来解读带入参数，类似于bash里面执行指令里面的 bash xx.sh $1 $2...
	#同理，sys.argvs[0] 指的是python程序本身，sys.argvs[1] 就指的python后面跟的第一个参数，sys.argvs[2] 指的是第二个参数，依次类推
	global oam_ip,oam_usr,oam_pwd,log_level,tti_on, tti_len,tti_max,local_level,rap
	host_ok = False
	i=0
	while i < len(sys.argv):
		if i==0: 
			i+=1
			continue
		if sys.argv[i].startswith('-h') or sys.argv[i].startswith('--h'):
			print info
		#如果第一个参数是-h or --h就打印注释，并切退出程序
			sys.exit()
		elif sys.argv[i].startswith('-s') or sys.argv[i].startswith('--s'): #small
			log_level = LEVEL_MIN
		#如果是-s的话，就设置log_level
		elif sys.argv[i].startswith('-f') or sys.argv[i].startswith('--f'): #full
			log_level = LEVEL_FULL
		elif sys.argv[i].startswith('-d') or sys.argv[i].startswith('--de'): #debug
			local_level = logging.DEBUG			
		elif sys.argv[i].startswith('-r') or sys.argv[i].startswith('--r'): #rap	
			if i+1 < len(sys.argv):
				ip = re.findall('((?:[0-9]{1,3}\.){3}[0-9]{1,3})',sys.argv[i+1])
				if ip:
					rap = ip[0]
				else:
					print "RAP IP address is invalid!\n"
					print info
					sys.exit()
				i+=2
				continue
		elif sys.argv[i].startswith('-t') or sys.argv[i].startswith('--t'): #tti
		#暂时不看tti怎么弄的0129
			tti_on = TTI_INCLUDE
			if i+1 < len(sys.argv) and sys.argv[i+1].isdigit():
				tti_len = int(sys.argv[i+1]	)
				if tti_len > tti_max:
					print 'Trace time for tti should not exceed ' + str(tti_max) + ' seconds!\n'
					sys.exit()
				elif tti_len <=0:
					print "0 second's trace time, will be quit.\n"
					sys.exit()					
				tti_on = TTI_ONLY
				i +=2
				continue
		elif host_ok:
			oam_pwd=sys.argv[i]			
		elif '@' in sys.argv[i]:
			hname = sys.argv[i].split('@')
			if hname[0] is not '':
				oam_usr = hname[0]
				host_ok = True
			if hname[1] is not '':
				oam_ip = hname[1]
				host_ok = True
		else:
			oam_ip = sys.argv[i]
			host_ok = True
		i+=1
		
	#print 'omu:'+oam_ip+' pwd:'+oam_pwd+' level:'+str(log_level) +' tti:'+ str(tti_on)+','+str(tti_len)
	#sys.exit()  
	return host_ok
	
def bat_logs(i,j):
	global hosts,t_runtime
	logging.debug('bat log i,j:' + str(i) +',' +str(j))
	if j<0 or i > j:
		logging.error('bat log quit in i,j:' + str(i) +',' +str(j))
		return 1
	threads = []
	while i<=j:
		if hosts[i]:
			ret, hosts[i]['conn'], hosts[i]['chan'] = start_ses()
			#为什么又开始ssh到oam去？？啥意思？
			#A: 为了进其他的 VM和DU，同一都先进入oam
			if ret:
			#进这个if就说明ssh到oam失败了
				logging.error(hosts[i]['name'] + ' starting failed:' + str(ret) + ', skipped!')
				i+=1
				continue
			if login_target(hosts[i], hosts[i],False,owner):
			#分别进入各个hosts，如果能进去，则返回0，则不进此if
				logging.error("_" + hosts[i]['name'] + " login failed, skipped!")
				i+=1
				continue
			
			if hosts[i].has_key('skip'):
				if hosts[i]['skip']:
					logging.info("_" + hosts[i]['name'] + " skipped!")
					i+=1
					continue
									
			clean_up(hosts[i],0,hosts)
			#这儿为啥要JBclean？？？？？？
			#A:这里的clean file是1，与之前带0是不一样的，搞懂了这两个的区别，应该能理解为什么这里要clean了
			hosts[i]['files'] = 0
					
			hosts[i]['th'] = threading.Thread(target=log_r, args=(hosts[i], hosts))
			#这里的target是要执行方法，后面的args是要传入的参数
			#疑问，后面的thread既然不返回什么东西，怎么把后面这坨赋值给这个host[i]['th']??
			threads.append(hosts[i]['th'])
			logging.info( "_" + hosts[i]['name'] + " thread ready: " + hosts[i]['th'].getName() )
			logging.debug(hosts[i])			
		i+=1
			
	for t in threads:
		t.setDaemon(True)
		t.start()
	
	#for t in threads:
	#	t.join(MAX_RUNTIME)
	#for t in threads:
	#	if t.isAlive(): 
	#		logging.error("___ thread failed! " + t.getName() )
	#		return 2
	
	#lpdt
	while True:
		time.sleep(1)
		t_runtime += 1
		alive = False
		for t in threads:
			alive = alive or t.isAlive()
		if not alive:
			break
		show_t_bars()
		if t_runtime > MAX_RUNTIME:
			logging.fatal("___ thread timedout! " + t.getName() )
			break
				
	logging.info("round done!")
	return 0

def ProgressBar(Bar, Progress, Total=50, BarLength=50, ProgressIcon="#", BarIcon="-"):
    try:
        # You can't have a progress bar with zero or negative length.
        if BarLength <1:
            BarLength = 20
        # Use status variable for going to the next line after progress completion.
        Status = ""
        # Calcuting progress between 0 and 1 for percentage.
        Progress = float(Progress) / float(Total)
        # Doing this conditions at final progressing.
        if Progress >= 1.:
            Progress = 1
            Status = "\r\n"    # Going to the next line
        # Calculating how many places should be filled
        Block = int(round(BarLength * Progress))
        # Show this
        Bar = Bar.format(ProgressIcon * Block + BarIcon * (BarLength - Block), round(Progress * 100, 0), Status)
        sys.stdout.write(Bar)
        
    except Exception as e:
        return e

def show_t_bars():
	if os.name == 'nt':
		cl = 'cls'
	else:
		cl = 'clear'		
	os.system(cl)

	for i in range(len(hosts)):
		ProgressBar(hosts[i]['bar'], hosts[i]['bar_i'])
	sys.stdout.flush() 

def post_pre_cfg(omu_int_ip):
	global hosts
	for i in range(0,len(hosts)):
		if hosts[i]['name'] == 'fctla':
			hosts[i]['om'] = omu_int_ip
				
			
if __name__=="__main__":
	start = datetime.datetime.now()
	
	if not handle_argvs():
	#这里的if not是为了，当输入不带IOAMIP地址时，直接使用ip a去读取oam的ip(此场景用于把此脚本放在OAM VM上执行的情况)
		ip = get_if(None,None,None,'oam')
		if ip:
			oam_ip = ip

	#如果带参数了，或者指定了oam_ip应该是不走进这个if not里面的
	log_setup(local_level)
	#记录debug log
	#判断oam ip是否正常,如果在参数不带oam IP，且不在文件中加OAM IP，那么oam=''，那么就会走到这个if not 里面来
	if not oam_ip:
		print '***No gNB host name or IP address is given, aborted!\n\n'
		print info		
		sys.exit()
	#打印文件执行记录log
	sys.stdout.write('GNB_Logs, V'+str(version) + '\n')			
	logging.info ("Collect GNB logs v" + str(version) +" from "+oam_ip +", Level=%d," % log_level + "Start: %s" % start.ctime())
	logging.debug(sys.argv)
	#可以用ctrl + : 来查关键字，可以查到此处的owner是个字典
	owner['name'] = "OAM-0"
	owner['prompt'] = "$ "
	owner['prompt_kw'] = 'oam-0'
	ret, owner['conn'], owner['chan'] = start_ses()
	#start_ses用于引入paramiko.sshclient 用于ssh到oam 的环境上
	owner['oam'] = oam_ip
	#获取oam的ip
	owner['internal'] = get_if(owner['chan'],owner['name'],owner['prompt'],'internal')
	#获取internal的IP
	owner['fronthaul'] = get_if(owner['chan'],owner['name'],owner['prompt'],'fronthaul')
	#获取fronthaul的IP

	logging.debug(owner)
	
	get_cu_hosts(owner,rap)		
	#感觉是去登陆到CU的VM，但是里面有登陆到DU的用户名和信息，不知道为啥
	#主要是去让hosts这个list里面填上VM的host，以及DU的host的字典信息
	clean_up(owner,1,hosts)
	#删除hosts里面存下来的，但是存在哪儿的，现在还不明白
	#懂了，是为了把之前可能留下来的log给删除，删的是OAM_*
	for i in range(0, len(hosts)):
	#如果前面有填rap的话，这里就会进来，然后再获取一波du的hosts
		if hosts[i]:
			if 'fctla' in hosts[i]['name']:				
				get_du_hosts(owner,hosts[i])
				add_rap_rout(owner,hosts[i])
	
	#if len(hosts) < 
	for i in range(len(hosts)):
		hosts[i]['files'] = 0
		hosts[i]['bar'] = '{:<6}'.format(hosts[i]['name']) + ": [{}] {:.0f}% {}\n"
		#这是在干嘛呢？？？
		hosts[i]['bar_i'] = 0
		if 'fctlb' in hosts[i]['name']:
			hosts[i]['pre'] = bb2_misc_logs 
			if not tti_on == TTI_NONE:
				ret = tti_gen(owner,hosts[i])
		if 'fctla' in hosts[i]['name']:
			hosts[i]['pre'] = asik_misc_logs	
			
	if not tti_on == TTI_ONLY:
		ret = run_log_r()
		#开多线程，收集log

	log_download(owner, hosts)
	#这个没有完全仔细看。2.2
	#clean_up(node, all_files, nodes)
	close_ses(owner)
	
	end = datetime.datetime.now()
	logging.info("End : %s" % end.ctime())
	logging.info("Duration seconds: %s",(end - start).seconds)	

#疑问1：他为啥要获得internal的IP？？拿来干啥
#A: 好像是在这里get_cu_hosts里用到了h['om'] = owner['internal']，但是为啥要获得这个东西，还是不明白
#A: 好像是为了在这个里面add_rap_rout，去给RU加route的
#疑问2: #routr是什么东西？？哪儿来的？？？0129
#A: 它好像是在这加路由，用internal网络从CU到DU，感觉这个B很有想法
#疑问3: 454行 试图从channel的shell里ssh到DU，但是现在我是在oam还是在本身的电脑上，我还没搞清楚
#疑问4: 1076行 #感觉是去登陆到CU的VM，但是里面有登陆到DU的用户名和信息，不知道为啥
#疑问5: #这里为什么会用shell去删除这些host，难道在哪儿保存了下来？？
#A： 懂了，是为了把之前可能留下来的log给删除，删的是OAM_*
#疑问6: #最后会尝试进入DU，然后获得rlan0的IP，为什么要获得rlan0的ip，是为了进abil？？
#疑问7: #oam_max_ses =10这个10它是怎么得来的，这个ses是指的session吗？？
#疑问8: #疑问，后面的thread既然不返回什么东西，怎么把后面这坨赋值给这个host[i]['th']??
