#!/bin/bash
#ssh toor4nsn@192.168.253.52 "fpga-cli regr 2 0x001F0014|sed -n '2p'">val.log
haha=`ssh toor4nsn@192.168.253.52 "fpga-cli regr 2 0x001F0014|sed -n '2p'"`
echo $haha
#################################################################
##could use arguement straightly but write in to the val.log!!!##
#################################################################

#val=`cat val.log| awk -F : '{print $2}'`
#echo $val

#if [ $val = "0x1001f10f" ]; then
#    echo "ABIK L1 CPRI status good"
#else
#    echo "failed, man ,check it."
#       cat /tmp/startup_NODEOAM.log | grep "CPRI link"
#fi




