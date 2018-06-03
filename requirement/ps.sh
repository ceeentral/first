#!/bin/bash

oamadd=192.168.253.1:/root/
day=$(date| awk '{print $2$3}')
tm=$(date| awk '{print $4}'| awk -F: '{print $1$2}')
lgps=${day}slave${tm}.log

bsh 1
journalctl -ab>${lgps}
scp ${lgps} ${oamadd}
#first logic journal grab

