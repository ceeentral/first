#!/bin/bash
du=172.18.5.32
pswd='oZPS0POrRieRtu'
#set time 10
val1=`cat /var/opt/nokia/lib/internalsshkeys/robot/id_rsa.pub`

(/usr/bin/expect <<EOF
spawn -noecho ssh  -o BatchMode=no -o PasswordAuthentication=yes -o PreferredAuthentications=password toor4nsn@$du
expect "*password:*" {send "$pswd\r"}
expect "*fctl*" {send "pwd\r"}
expect "*fctl*" {send "echo $val1 >> /user/toor4nsn/.ssh/authorized_keys\r"} 
expect "*fctl*" {send "exit\r"}
expect eof

EOF
) >ep.log 2>&1 #hide expect output to ep.log
ssh toor4nsn@172.18.5.32
