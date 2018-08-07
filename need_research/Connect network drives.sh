#!/bin/bash
#author Karim Harouat



txzfile=`find /ffs/run/boardcfg -name "*.txz"`
tgzfile=`find /ffs/run/boardcfg -name "*.tgz"`
files="$txzfile $tgzfile"

for i in  $files  ; do
    set +e
    tar tvf $i | grep -E "tmp/(RTCCSConfig|CCSEarlyConfig).xml"  1>/dev/null 2>/dev/null
    if [ ${PIPESTATUS[1]} -eq 0 ]
    then
        filesxml=$(tar tvf $i | grep -E "tmp/(RTCCSConfig|CCSEarlyConfig).xml" | awk '{print $6}' | tr ['\n'] [' '])
        echo "$i has $filesxml xml file "
    fi
    set -e
done
