#!/bin/bash
# Bei Start über ein Script (kein systemd-Service)
# wird eine Datei mit der Prozess-ID erzeugt.
# Damit lässt sich der Libre-Office-Server bei Bedarf beenden,
# wenn er sich nach Strg-C nicht automatisch beendet.
if [ -e run/soffice.pid ]
then
echo "pid entfernen"
PID=$(cat run/soffice.pid)
echo $PID
kill -9 $PID
rm run/soffice.pid
fi
