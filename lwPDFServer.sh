#!/bin/bash
SCRIPTPATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
# Python Version bei Bedarf anpassen
# PYDIR=python-core-3.8.19
source Python_version
# LibreOffice.org als Server starten
lo=$(ps ax | grep "soffice.bin --headless" | grep -v grep)
if [ "$lo" ]
then
echo "LibreOffice-Server läuft bereits"
else
echo "Starte Libre Office"
libreoffice/program/soffice --headless --nologo --nodefault --nofirststartwizard --pidfile=$SCRIPTPATH/run/soffice.pid --accept="socket,host=localhost,port=2002;urp;" &
# --nologo --nodefault --nofirststartwizard startet Libre Office ohne sichtbares Fenster
echo "Bitte warten..."
# Libre Office etwas Zeit für den Start geben
sleep 10
PID=$(cat run/soffice.pid)
echo "Libre Office mit PID: "$PID" gestartet"
fi

PATH=$SCRIPTPATH/libreoffice/program:$SCRIPTPATH/libreoffice/program/$PYVER/bin:$PATH
cd $SCRIPTPATH/lwPDF
# Zeile für den manuellen Start
echo "Starte $SCRIPTPATH/libreoffice/program/python $SCRIPTPATH/libreoffice/program/$PYDIR/bin/webware serve -b"
exec $SCRIPTPATH/libreoffice/program/python $SCRIPTPATH/libreoffice/program/$PYDIR/bin/webware serve -b
# Zeile für den Start über einen systemd-Dienst
# Der Server soll im Netzwerk erreichbar sein
# name-des-Servers-oder-IP anpassen
#exec $SCRIPTPATH/libreoffice/program/python $SCRIPTPATH/libreoffice/program/$PYDIR/bin/webware serve -l name-des-Servers-oder-IP --prod

