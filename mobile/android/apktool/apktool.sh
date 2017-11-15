#!/bin/bash
DIR=~/opt/sectools/mobile/android/apktool/
if [ "$1" == "--check-update" ]; then
	latest=$(curl -s https://api.github.com/repos/iBotPeaches/Apktool/releases/latest | jq -r ".assets[] | select(.name | test(\"${spruce_type}\")) | .browser_download_url")
	if [ -e ${DIR}/`basename ${latest}` ]; then 
		echo "up to date: `basename ${latest}`"
		exit 0
	else
		echo "Downloading: ${latest}"
		curl -L ${latest} -o ${DIR}/`basename ${latest}`
		exit 1
	fi
fi
java -jar $(find ${DIR} -name 'apktool_*' | sort | tail -n 1) $@