#!/bin/bash

#rq=`date + "%m%d"`
#sj=`date + "%H%M"`
day=$(date|awk '{print $2$3}')
tm=$(date|awk '{print $$4}' |awk -F: '{print $1$2}')
pfr=${day}${tm}fr.pcap
ssh cpif-0.local "sudo tcpdump -i fronthaul -c 10 -w ${pfr} -vv && scp ${pfr} oam-0.local:/home/robot/"
