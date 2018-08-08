#!/bin/bash
ssh fsp-1-1c "fpga_rw ra 0xdf201004">val.log
val=`cat val.log`
echo $val

if [ $val = "0x00000010" ]; then
    echo "ABIL1 L1 CPRI status good"
else
    echo "ABIL1"
    echo "failed, man ,check it1."
	cat /tmp/startup_NODEOAM.log | grep "CPRI link"
fi

ssh fsp-1-2c "fpga_rw ra 0xdf201004">val.log
val=`cat val.log`
echo $val
if [ $val = "0x00000010" ]; then
    echo "ABIL2 L1 CPRI status good"
else
    echo "the ABIL2"
    echo "failed, man ,check it."
        cat /tmp/startup_NODEOAM.log | grep "CPRI link"
fi


ssh fsp-1-3c "fpga_rw ra 0xdf201004">val.log
val=`cat val.log`
echo $val
if [ $val = "0x00000010" ]; then
    echo "ABIL3 L1 CPRI status good"
else
    echo "ABIL3"
    echo "failed, man ,check it."
        cat /tmp/startup_NODEOAM.log | grep "CPRI link"
fi

