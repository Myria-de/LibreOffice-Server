#!/bin/bash
# Konfiguration #
# Bei einer anderen Libre-Office-Version als 24.2.4 bitte
# in der Datei ../Python_version anpassen
#PYDIR=python-core-3.8.19
#PYVER=python3.8
source ../Python_version
# Konfiguration Ende #
SCRIPTPATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
PARENTDIR="$(dirname "$SCRIPTPATH")"
PATH=$SCRIPTPATH/libreoffice/program:$SCRIPTPATH/libreoffice/program/$PYVER/bin:$PATH
# Installationsscript für Python-PIP herunterladen
wget https://bootstrap.pypa.io/get-pip.py

if [ ! -e get-pip.py ]
then
echo "Konnte get-pip.py nicht herunterladen. Bitte URL prüfen."
exit 1
fi
# pip installieren
if [ -e $PARENTDIR/libreoffice/program/python ]
 then
 PATH=$PARENTDIR/libreoffice/program/$PYDIR/bin:$PATH
 $PARENTDIR/libreoffice/program/python get-pip.py
 #Zusätzliche Ptyhon-Module installieren
 $PARENTDIR/libreoffice/program/python -m pip install waitress "Webware-for-Python>=3"
 $PARENTDIR/libreoffice/program/python -m pip install matplotlib
 $PARENTDIR/libreoffice/program/python -m pip install requests
 #fix for the moment "No module named 'numpy.core._multiarray_umath" in numpy
 $PARENTDIR/libreoffice/program/python -m pip install numpy==1.21.0

 # fix .so names ABI
 # LibreOffice-Python uses cpython-XX, while pip uses .cpython-XX-x86_64-linux-gnu.so
 PKGDESTDIR=$PARENTDIR/libreoffice/program/$PYDIR/lib/$PYVER/site-packages
 find "${PKGDESTDIR}" -type f -executable -iname '*.cpython*.so' \
        | while read -r file; do
        filename="${file##*/}"
        modulename="${filename%%.*}"
        echo "${pkgver}: renamed '${filename}' to '${modulename}.so'.\n"
        ln -s ${file} ${file%/*}/${modulename}.so
 done

else
 echo "Libre Office nicht gefunden. Bitte mit 1_Get_LO_Portable.sh installieren."
 exit 1
fi




