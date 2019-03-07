#!/usr/bin/bash
if [[ -e res.bin.xz ]];then
	rm res.bin.xz
fi

scp snapshot_tx0_320slots fsp-1-1c:/home/toor4nsn
ssh fsp-1-1c "chmod +x snapshot_tx0_320slots && ./snapshot_tx0_320slots && exit"
sleep 10
ssh fsp-1-1c "memdump --count 0x4CCCCCC --file res.bin 0x80000000"
sleep 5m
scp fsp-1-1c:/home/toor4nsn/res.bin .
xz res.bin
