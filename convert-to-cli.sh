#!/bin/bash
# Beispiel für die Nutzung auf der Kommandozeile
# Datei in das PDF-Format umwandeln.
OUTDIR="$HOME/Dokumente"
SCRIPTPATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"

if [ -z $1 ] 
then
echo "Fehler: Geben Sie eine Datei an, die Sie konvertieren möchten"
exit 1
fi

if [ -e $1 ]
then
libreoffice/program/soffice --convert-to pdf $1 --outdir $OUTDIR 
#--headless

else
echo "Fehler: Die Datei $1 existiert nicht."
fi

