#!/bin/bash


day=$(date| awk '{print $2$3}')
tm=$(date| awk '{print $4}'| awk -F: '{print $1$2}')
lgps=${day}slave${tm}.log

bsh 1 "journalctl -ab>${lgps} && scp -o StrictHostKeyChecking=no ${lgps} toor4nsn@192.168.253.1:/tmp/ && rm ${lgps} && exit "
ssh toor4nsn@192.168.253.20

