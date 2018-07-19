#!/bin/bash
ssh cpif-0.local "sudo tcpdump -i backhaul -w cuifX2.pcap -vv && exit"



