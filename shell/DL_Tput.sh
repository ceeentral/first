#!/bin/sh

sleeptime=10
prevValue=0
while [ 1 -gt 0 ]; do

	        newValue=`cat /opt/AirPhone/L2/L2Counter.txt | grep "DlSchDrbBytesCounter" | awk -F '[' '{ print $2 }' |tail -1 | awk -F ']' '{ print $1 }'`

		        instantdl=`expr $newValue - $prevValue`
			        prevValue=$newValue;
				        instantdl=`expr $instantdl \* 8`
					        instantdl=`expr $instantdl / $sleeptime `
						        echo "At : `date` DL bits/s=$instantdl"
							        sleep $sleeptime
							done
