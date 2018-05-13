#!/bin/bash
#ss=207.148.110.222


function Ping(){
	for ip in $(cat $1 | sed "/^#/d")
	do
		ping -c 2 $ip >>/Users/central/script/log
	    a=$?
		sleep 1
		ping -c 2 $ip >>/Users/central/script/log
		b=$?
		sleep 1
		Date=$(date +%F" "%H:%M) 
		if [ $a -ne 0 -a $b -ne 0 ] ; then
			echo  "Date : $Date\nHost : $ip\nProblem: ping failed"
		fi
    done
}

start(){
	if [["$# -lt 1"]]
		then
		Ping Fasttrack
		Ping 577-step2
	fi
	if [["$# -ge 2"]]
		then
		echo "please input right patameter!"
	fi
}

usage(){
	echo "haha, foolish! try 'test.sh -h' "
}

hhelp(){
	echo "********************************"
	echo "-F ping ip of Fasttrack "
	echo "-5 ping ip of 577-step2 "
	echo "-h help"
	echo "-v version "
	echo "********************************"
}

if [ "$#" -eq 0 ]; then
        usage
        exit 0
fi

case $1 in 
	-h|help )
	hhelp
	exit 0;
	;;
	-v|version )
	echo 'chuanchuan ping Version 0.1, 2018-05-05, Copyright (c) 2018 chuancuhan'
	exit 0;
	;;
esac

#check_user='whoami'
#if [ "$check_user" != "root" ]; then
#	echo 'must login with root account'
#	exit 1;
#fi

case $1 in
	-F|Fasttrack )
	Ping Fasttrack
	;;
	-5|577-step2 )
	Ping 577-step2
	;;
	* )
	usage
	;;
esac


#for ip in $(cat Fasttrack | sed "/^#/d")
#	do
#		
#		ping -c 2 $ip >>/Users/central/script/log
#	    a=$?
#		sleep 1
#		ping -c 2 $ip >/dev/null
#		b=$?
#		Date=$(date +%F" "%H:%M) 
#		if [ $a -ne 0 -a $b -ne 0 ] ; then
#			echo  "Date : $Date\nHost : $ip\nProblem: ping failed"
#		fi
#done
##	将与以 '#' 开始的任何行匹配 d表示删除，此命令意思是把注释行都删掉
##ping $ss >/dev/null 2>&1
#echo $?
#if [$?]
