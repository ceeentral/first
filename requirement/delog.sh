#!/bin/bash
#this is for debian emu delete log
cd ap128_gnb166/wts
rm -rf egate.log* enb_1.log* mme_1.log* pgw_1.log* sgw_1.log* stdout_* uec_1.log* egate.log* error_*

cd ../uec
rm -rf egate.log*  stdout_*
