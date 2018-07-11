#!/bin/bash
ssh upue-0.local "sudo tcpdump -i backhaul -w cuupueX2.pcap -vv && sudo tcpdump -i fronthaul -w cuupueF1.pcap -vv"