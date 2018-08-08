#!/bin/bash
#author chuan

day=$(date| awk '{print $2$3}')
tm=$(date| awk '{print $4}'| awk -F: '{print $1$2}')

function tcpcpif(){
	(ssh cpif-0.local "sudo tcpdump -i backhaul -w ${day}ifBH.pcap" &) 
	(ssh cpif-0.local "sudo tcpdump -i fronthaul -w ${day}ifFT.pcap" &)
	
}

function tcpupue(){
	(ssh upue-0.local "sudo tcpdump -i backhaul -w ${day}upBH.pcap" &) 
	(ssh upue-0.local "sudo tcpdump -i fronthaul -w ${day}upFT.pcap" &)
	
}
function killif(){
	ssh cpif-0.local "ps -ef |grep ${day}ifBH.pcap ">aa.log
	val1=`cat aa.log|sed -n '1p'|awk '{print $2}'`
	echo $val1
	ssh cpif-0.local "ps -ef |grep ${day}ifFT.pcap ">aa.log
	val2=`cat aa.log|sed -n '1p'|awk '{print $2}'`
	echo $val2
	ssh cpif-0.local "sudo kill $val1 $val2"

}

function killup(){
        ssh upue-0.local "ps -ef |grep ${day}upBH.pcap ">aa.log
        val1=`cat aa.log|sed -n '1p'|awk '{print $2}'`
        echo $val1
        ssh upue-0.local "ps -ef |grep ${day}upFT.pcap ">aa.log
        val2=`cat aa.log|sed -n '1p'|awk '{print $2}'`
        echo $val2
        ssh upue-0.local "sudo kill $val1 $val2"


}


function usage(){
	echo "#####################################"
	echo "-h help     :usage  "
	echo "-a all      :start a process to grab cpif&upue FH&BH pcap at the same time"
	echo "-i|cpif     :ssh cpif and start to tcpdump "
	echo "-ki  	      :kill cpif's 2 tcpdump process"
	echo "-u|upue     :ssh upue and start to tcpdump"
	echo "-ku         :kill upue's 2 tcpdump process"
	echo "#####################################"
}



if [[ $# -eq 0 ]];then
    tcpcpif
else
    case $1 in 
	-h|help )
	    usage
	    exit 0;
	    ;;
	-v|version )
	    echo 'chuanchuan  Version 0.1, 2018-08-08, Copyright (c) 2018 chuancuhan'
        ;;
	-ki )
		killif
		;;
	-ku )
		killup
		;;
	-a|all )
	    tcpcpif
		tcpupue
	    ;;
	-i|cpif )
		tcpcpif
		;;
	-u|upue )
		tcpupue
		;;
	* )
	    usage
	    ;;
esac
fi

#screen ssh cpif-0.local "sudo tcpdump -i fronthaul -w ${day}cpifFT.pcap -vv"
#ssh cpif-0.local "screen sudo tcpdump -i fronthaul -w ${day}cpifFT.pcap -vv "
#ssh cpif-0.local "screen sudo tcpdump -i backhaul -w ${day}cpifBH.pcap -vv && exit"
#screen ssh cpif-0.local "sudo tcpdump -i fronthaul -w ${day}ifFT.pcap &"
