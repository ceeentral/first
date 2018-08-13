#!/bin/bash
du=172.18.5.32
ABIL=fsp-1-1a
loner=fsp-1-1c
pswd='oZPS0POrRieRtu'
#set time 10
val1=`cat /var/opt/nokia/lib/internalsshkeys/robot/id_rsa.pub`
day=$(date| awk '{print $2$3}')
tm=$(date| awk '{print $4}'| awk -F: '{print $1$2}')
lgps=${day}slave${tm}.log
lghi=${day}master${tm}.log



function ps(){
echo "journalctl -ab>/tmp/${lghi}">ps.sh 
echo "bsh 1 'journalctl -ab>${lgps} && scp -o StrictHostKeyChecking=no ${lgps} toor4nsn@192.168.253.1:/tmp/ && rm ${lgps} && exit '">>ps.sh
}

function wrsa(){
(/usr/bin/expect <<EOF
spawn -noecho ssh  -o BatchMode=no -o PasswordAuthentication=yes -o PreferredAuthentications=password toor4nsn@$du
expect "*password:*" {send "$pswd\r"}
expect "*fctl*" {send "pwd\r"}
expect "*fctl*" {send "echo $val1 >> /user/toor4nsn/.ssh/authorized_keys\r"} 
expect "*fctl*" {send "exit\r"}
expect eof

EOF
) >ep.log 2>&1 #hide expect output to ep.log

}
#if your DU ip is ipv6, remember to use spawn -noecho ssh -6 -o BatchMode=no -o PasswordAuthentication=yes -o PreferredAuthentications=password toor4nsn@$du
#ssh -6 -q toor4nsn@$du
ps
scp -q ps.sh toor4nsn@$du:~
if [ $? == 1 ]
then
wrsa
ssh -q toor4nsn@$du "sh ps.sh && cd /tmp && tar zcf du.tgz ${lghi} ${lgps} startup*"
else
ssh -q toor4nsn@$du "sh ps.sh>/dev/null 2>&1 && cd /tmp && tar zcf du.tgz ${lghi} ${lgps} startup* && ls -al|grep du.tgz"

fi



