#!/bin/bash
shelluser=test
shellpaswd=a!Anoeric12
openproject=TEST
openuser=xiaowang
openpaswd=shixiaowang

source /etc/nova/openrc
openstack project create $openproject
openstack user create $openuser --project $openproject --password $openpaswd
openstack role add --project $openproject --user $openuser admin



echo "chuanNokia1!!" | sudo -S adduser $shelluser
sudo passwd "$shelluser" <<< "$shellpaswd"$'\n'"$shellpaswd"
#2 different ways to input password, and use <<< can input it twice. that's really nb.

sudo cp /etc/nova/openrc /home/$shelluser/${shelluser}rc
sudo sed "s/OS_USERNAME.*/OS_USERNAME=$openuser/" -i /home/$shelluser/${shelluser}rc
sudo sed "s/OS_PASSWORD.*/OS_PASSWORD=$openpaswd/" -i /home/$shelluser/${shelluser}rc
sudo sed "s/keystone_admin/$shelluser/" -i /home/$shelluser/${shelluser}rc
sudo sed "s/OS_PROJECT_NAME.*/OS_PROJECT_NAME=$openproject/" -i /home/$shelluser/${shelluser}rc
sudo chown $shelluser:$shelluser /home/$shelluser/${shelluser}rc
sudo chmod 644 /home/$shelluser/${shelluser}rc

source /home/$shelluser/${shelluser}rc
openstack keypair create keypair

