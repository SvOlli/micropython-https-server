#!/bin/sh

readonly port="/dev/ttyUSB0"

set -e
cd "$(dirname "${0}")"

if [ ! -f wifi.txt ]; then
   echo "wifi.txt not found, creating one"
   echo -n "SSID: "
   read ssid
   echo -n "Pass: "
   read pass
   echo "${ssid}" > wifi.txt
   echo "${pass}" >> wifi.txt
fi

if [ ! -f cert/example.crt -o ! -f cert/example.key ]; then
   echo "certificate and or key not found, creating a new pair"
   cert/create_cert.sh
fi

for i in HTTPSServer.py main.py favicon.ico wifi.txt cert/example.crt cert/example.key; do
   [ -f "${i}" ] || continue
   ls -l "$(readlink -f "${i}")"
   ampy -p "${port}" put "${i}"
done
ampy -p "${port}" ls -l
ampy -p "${port}" run reset.pyi 2>/dev/null || :
case "${1}" in
term) exec microcom -p "${port}";;
esac
