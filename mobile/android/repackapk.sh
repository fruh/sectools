#!/bin/bash
if [ "$1" == "" -o "$2" == "" ]; then
	echo "usage: repackapk src app.apk"

	exit 1;
fi

if [ -e "$2" ]; then
	echo "Remove ${2}? [y/n]"

	read option

	[ "$option" == "y" ] && rm -v "$2" || exit 1
fi

if [ ! -e "$1" ]; then
	echo "'${1}' does not exists"
	exit 1
fi

DECOMPILED="$1"
OUTPUT="$2"
KEYFILE=/tmp/repackapk.keystore

apktool b "${DECOMPILED}" -o "${OUTPUT}-unalligned"
[ -e "$KEYFILE" ] || keytool -genkey -v -keystore "$KEYFILE" -alias alias_name -keyalg RSA -keysize 2048 -validity 10000
jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 -keystore "$KEYFILE" "${OUTPUT}-unalligned" alias_name
jarsigner -verify -verbose -certs "${OUTPUT}-unalligned"
zipalign -v 4 "${OUTPUT}-unalligned" "${OUTPUT}"
