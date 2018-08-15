#!/usr/bin/bash
#adapt to your own enviroment info for below variable##
du=fc00::172:18:5:35
ABIL=fsp-1-1a
loner=fsp-1-1c
#adapt your du,ABIL and loner's hostname, you can use arp -a to check the hostname
pswd='oZPS0POrRieRtu'

day=$(date| awk '{print $2$3}')
tm=$(date| awk '{print $4}'| awk -F: '{print $1$2}')
lgps=${day}du_slave${tm}.log
lghi=${day}du_master${tm}.log
lgif=${day}cpif_journal${tm}.log
lgue=${day}cpue_journal${tm}.log
lgcl=${day}cpcl_journal${tm}.log
lgnb=${day}cpnb_journal${tm}.log
lgup=${day}upue_journal${tm}.log
lgom=${day}oam_journal${tm}.log


function ps(){
	echo "journalctl -ab>/tmp/${lghi}">ps.sh 
	echo "bsh 1 >/dev/null 2>&1 'journalctl -ab>${lgps} && scp -o StrictHostKeyChecking=no ${lgps} toor4nsn@192.168.253.1:/tmp/ && rm ${lgps} && exit '">>ps.sh
	echo "scp -q $loner:/var/log/l1sw-startup.log.gz /tmp/">>ps.sh
	echo "scp -q $ABIL:/tmp/ASPA* /tmp/ ">>ps.sh
	echo "cd /tmp ">>ps.sh
	echo "tar zcf du.tgz ${lghi} ${lgps} startup*  l1sw-startup.log.gz ASPA*  ">>ps.sh
}

function wrsa(){
rsakey=`cat /var/opt/nokia/lib/internalsshkeys/robot/id_rsa.pub`
if [ $1 == v6 ]
then
(/usr/bin/expect <<EOF
	spawn -noecho ssh -6 -o BatchMode=no -o PasswordAuthentication=yes -o PreferredAuthentications=password toor4nsn@$du
	expect "*password:*" {send "$pswd\r"}
	expect "*fctl*" {send "pwd\r"}
	expect "*fctl*" {send "echo $rsakey >> /user/toor4nsn/.ssh/authorized_keys\r"} 
	expect "*fctl*" {send "exit\r"}
	expect eof

EOF
) >ep.log 2>&1 #hide expect output to ep.log
else
(/usr/bin/expect <<EOF
	spawn -noecho ssh  -o BatchMode=no -o PasswordAuthentication=yes -o PreferredAuthentications=password toor4nsn@$du
	expect "*password:*" {send "$pswd\r"}
	expect "*fctl*" {send "pwd\r"}
	expect "*fctl*" {send "echo $rsakey >> /user/toor4nsn/.ssh/authorized_keys\r"} 
	expect "*fctl*" {send "exit\r"}
	expect eof

EOF
) >ep.log 2>&1 #hide expect output to ep.log
fi
}


function getcu(){
	ssh -q cpif-0.local "sudo journalctl -ab>${lgif} && scp ${lgif} oam-0.local:/home/robot/ && rm ${lgif} && ' scp *.pcap oam-0.local:/home/robot/ '>/dev/null 2>&1 && rm *.pcap && exit "
	ssh -q cpue-0.local "sudo journalctl -ab>${lgue} && scp ${lgue} oam-0.local:/home/robot/ && rm ${lgue} && exit "
	ssh -q cpcl-0.local "sudo journalctl -ab>${lgcl} && scp ${lgcl} oam-0.local:/home/robot/ && rm ${lgcl} && exit "
	ssh -q cpnb-0.local "sudo journalctl -ab>${lgnb} && scp ${lgnb} oam-0.local:/home/robot/ && rm ${lgnb} && exit "
	ssh -q upue-0.local "sudo journalctl -ab>${lgup} && scp ${lgup} oam-0.local:/home/robot/ && rm ${lgup} && sudo scp /tmp/LINUX_startup.log oam-0.local:/home/robot/LINUX_startup_UPUE.log && ' scp *.pcap oam-0.local:/home/robot/  '>/dev/null 2>&1 && rm *.pcap && exit"
	sudo journalctl -ab>${lgom}
	cp /opt/nokia/SS_MzOam/cloud-racoam/logs/startup_RACOAM.log ./CU_startup_RACOAM.log
	cp /opt/nokia/SS_MzOam/cloud-siteoam/siteoam/logs/startup_SITEOAM.log ./CU_startup_SITEOAM.log
	if [[ -e log.zip ]];then 
		rm log.zip
	fi
	zip -q log.zip du.tgz LINUX_startup_UPUE.log CU_startup_RACOAM.log CU_startup_SITEOAM.log ${lgom} ${lgup} ${lgnb} ${lgcl} ${lgue} ${lgif} *.pcap >/dev/null 2>&1
	rm -f *.log ps.sh du.tgz 

}





function getdu(){
ps
if [ $1 == v6 ]
then
	
	scp -6 -q ps.sh toor4nsn@\[$du\]:~
	if [ $? == 1 ]
	then
		wrsa v6
		scp -6 -q ps.sh toor4nsn@\[$du\]:~
		ssh -6 -q toor4nsn@$du "sh ps.sh"
		scp -6 -q toor4nsn@\[$du\]:/tmp/du.tgz .
	else
		ssh -6 -q toor4nsn@$du "sh ps.sh"
		scp -6 -q toor4nsn@\[$du\]:/tmp/du.tgz .
	fi
else

	scp -q ps.sh toor4nsn@$du:~
	if [ $? == 1 ]
	then
		wrsa
		scp -q ps.sh toor4nsn@$du:~
		ssh -q toor4nsn@$du "sh ps.sh"
		scp -q toor4nsn@$du:/tmp/du.tgz .
	else
		ssh -q toor4nsn@$du "sh ps.sh"
		scp -q toor4nsn@$du:/tmp/du.tgz .
	fi
fi
}

function ddte(){
	rm -f *.log *.pcap *.tgz *.zip ps.sh 
}


function usage(){
	echo "#########################################################"
	echo "==================================================="
        echo "this script should use in your CU oam VM"
	echo "If no options specified, collect du and cu log to a log.zip"
	echo "please adapt your du ip firstly"
	echo "default du ip=172.18.5.32"
	echo "==================================================="
	echo "-h help     :usage  "
	echo "-d delete   :delete all the log, pcap, tgz, zip in oam VM"
	echo "-6 ipv6     :if your TL is ipv6, please adapt your DU ip "
	echo "-v version"
	echo "-g          :make your cu can ssh du"
	echo "#########################################################"
}


if [[ $# -eq 0 ]];then
	getdu v4
    getcu
else
    case $1 in 
	-h|help )
	    usage
	    exit 0;
	    ;;
	-v|version )
	    echo "3tral's log collector Version 1.0, 2018-08-07, Copyright (c) 2018 3tral"
        ;;
	-6 )
		getdu v6
		getcu
		;;
	-d|delete )
	    ddte
	    ;;
	-g )
            wrsa v6
            ;;
        * )
	    usage
	    ;;
	esac
fi

exit 0


