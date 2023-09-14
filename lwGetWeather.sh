#!/bin/bash
SCRIPTPATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
# Python Version bei Bedarf anpassen
PYVER=python-core-3.8.17
# Libre Office als Server starten
lo=$(ps ax | grep "soffice --headless" | grep -v grep)
if [ "$lo" ]
then
echo "Libre-Office-Server läuft bereits"
else
echo "Starte Libre Office"
# --nologo --nodefault --nofirststartwizard startet Libre Office ohne sichtbares Fenster
libreoffice/program/soffice --headless --nologo --nodefault --nofirststartwizard --pidfile=$SCRIPTPATH/run/soffice.pid --accept="socket,host=localhost,port=2002;urp;" &
echo "Bitte warten..."
# Libre Office etwas Zeit für den Start geben
sleep 10
PID=$(cat run/soffice.pid)
echo "LibreOffice mit PID: "$PID" gestartet"
fi

echo "Starte lwPDFConverter.py. Warte auf Dateien..."
echo "Beenden mit Strg-C"
libreoffice/program/python lwGetWeather.py

