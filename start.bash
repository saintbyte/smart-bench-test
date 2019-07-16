#!/bin/bash
set -x
hciconfig hci0 piscan
hciconfig hci0 name 'HC-05'
hciconfig hci0 noauth
hciconfig hci0 sspmode 1
bt-agent --capability=NoInputNoOutput --daemon
sdptool add SP
python3 main4.py