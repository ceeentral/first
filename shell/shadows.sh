#!/bin/bash

function toolsetup{
	command -V date >/dev/null 2>&1 || {echo >&2 "please confirm your server installed ubuntu system."; exit 1;}
  #  apt-get update >/dev/null 2>&1 || {if [$? -ne 1]; then
   # 	echo "tool install failed"
    #fi}
    apt-get install python-pip
    pip install --upgrade pip
    pip install setuptools
    if [$? -ne 1]; then
    	echo "tool install failed"
    fi
}

toolsetup