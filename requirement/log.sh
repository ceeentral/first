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

ssh cpif-0.local "sudo journalctl -ab>${lgif} && scp ${lgif} oam-0.local:/home/robot/ && rm ${lgif} && exit "
ssh cpue-0.local "sudo journalctl -ab>${lgue} && scp ${lgue} oam-0.local:/home/robot/ && rm ${lgue} && exit "
ssh cpcl-0.local "sudo journalctl -ab>${lgcl} && scp ${lgcl} oam-0.local:/home/robot/ && rm ${lgcl} && exit "
ssh cpnb-0.local "sudo journalctl -ab>${lgnb} && scp ${lgnb} oam-0.local:/home/robot/ && rm ${lgnb} && exit "
ssh upue-0.local "sudo journalctl -ab>${lgup} && scp ${lgup} oam-0.local:/home/robot/ && rm ${lgup} && exit "
journalctl -ab>${lgom}

#3tral

