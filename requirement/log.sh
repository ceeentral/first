#!/bin/bash

#vm list

#can also set time like this tt=`date +%F|awk -F- '{print$1$2$3}'`
day=$(date| awk '{print $2$3}')
tm=$(date| awk '{print $4}'| awk -F: '{print $1$2}')
lgif=${day}cpif_journal${tm}.log
lgue=${day}cpue_journal${tm}.log
lgcl=${day}cpcl_journal${tm}.log
lgnb=${day}cpnb_journal${tm}.log
lgup=${day}upue_journal${tm}.log
lgom=${day}oam_journal${tm}.log



function grab_log(){
	ssh cpif-0.local "sudo journalctl -ab>${lgif} && scp ${lgif} oam-0.local:/home/robot/ && rm ${lgif} && scp *.pcap oam-0.local:/home/robot/ && rm *.pcap && exit "
	ssh cpue-0.local "sudo journalctl -ab>${lgue} && scp ${lgue} oam-0.local:/home/robot/ && rm ${lgue} && exit "
	ssh cpcl-0.local "sudo journalctl -ab>${lgcl} && scp ${lgcl} oam-0.local:/home/robot/ && rm ${lgcl} && exit "
	ssh cpnb-0.local "sudo journalctl -ab>${lgnb} && scp ${lgnb} oam-0.local:/home/robot/ && rm ${lgnb} && exit "
	ssh upue-0.local "sudo journalctl -ab>${lgup} && scp ${lgup} oam-0.local:/home/robot/ && rm ${lgup} && sudo scp /tmp/LINUX_startup.log oam-0.local:/home/robot/LINUX_startup_UPUE.log && scp *.pcap oam-0.local:/home/robot/ && rm *.pcap && exit"
	sudo journalctl -ab>${lgom}
	cp /opt/nokia/SS_MzOam/cloud-racoam/logs/startup_RACOAM.log .
	cp /opt/nokia/SS_MzOam/cloud-siteoam/siteoam/logs/startup_SITEOAM.log .
}

function ddte(){
	rm -f *.log *.pcap
}
function usage(){
	echo "#####################################"
	echo "-h help     :usage  "
	echo "-a all      :collect all the log and pcap"
	echo "-d delete   :all the log and pcap in oam VM"
	echo "#####################################"
}

if [[ $# -eq 0 ]];then
    grab_log
else
    case $1 in 
	-h|help )
	    usage
	    exit 0;
	    ;;
	-v|version )
	    echo 'chuanchuan  Version 0.1, 2018-08-07, Copyright (c) 2018 chuancuhan'
        ;;
	-a|all )
	    grab_log
	    ;;
	-d|delete )
	    ddte
	    ;;
	* )
	    usage
	    ;;
esac
fi

exit 0