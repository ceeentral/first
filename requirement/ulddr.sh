#!/usr/bin/bash
if [[ -e captured_iq_data.bin.xz ]];then
	rm captured_iq_data.bin.xz
fi

scp UL_loner_tf0_iq_capture_disable_HARQ_long.sh fsp-1-1c:/home/toor4nsn
ssh fsp-1-1c "chmod +x UL_loner_tf0_iq_capture_disable_HARQ_long.sh && ./UL_loner_tf0_iq_capture_disable_HARQ_long.sh"
ssh fsp-1-1c "exit"
scp fsp-1-1c:/home/toor4nsn/ul_captured_iq_data.bin .
