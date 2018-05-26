#!/bin/bash

#vm list


day=$(date| awk '{print $2$3}')
tm=$(date| awk '{print $4}'| awk -F: '{print $1$2}')
lgif=${day}cpif${tm}.log
lgue=${day}cpue${tm}.log
lgcl=${day}cpcl${tm}.log
lgnb=${day}cpnb${tm}.log

ssh cpif-0.local "sudo journalctl -ab>${lgif} && scp ${lgif} oam-0.local:/home/robot/ && rm ${lgif} && exit "
ssh cpue-0.local "sudo journalctl -ab>${lgue} && scp ${lgue} oam-0.local:/home/robot/ && rm ${lgue} && exit "
ssh cpcl-0.local "sudo journalctl -ab>${lgcl} && scp ${lgcl} oam-0.local:/home/robot/ && rm ${lgcl} && exit "
ssh cpnb-0.local "sudo journalctl -ab>${lgnb} && scp ${lgnb} oam-0.local:/home/robot/ && rm ${lgnb} && exit "


#3tral

