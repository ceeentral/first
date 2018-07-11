#!/bin/bash
ssh toor4nsn@192.168.253.20 "fpga-cli regr 2 0x001F0014|sed -n '2p'">val.log
val=`cat val.log| awk -F : '{print $2}'`
echo $val

if [ $val = "0x1001f10f" ]; then
    echo "ABIK L1 CPRI status good"
else
    echo "failed, man ,check it."
fi



