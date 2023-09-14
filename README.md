# LibreOffice im Servermodus nutzen
Der Server-Modus von Libre Office bietet Schnittstellen, über die sich die Funktionen des Büropakets per Script nutzen lassen. Mit einem Webserver kann der Zugriff auch über das Netzwerk erfolgen.
## Libre Office und Python-Module einrichten
Kopieren Sie alle Dateien in Ihr Home-Verzeichnis, beispielsweise in den Ordner "~/lwPDF".

Die Installation von Libre Office erfolgt über ein Bash-Script, das Sie im Terminal im Ordner "~/lwPDF/install" mit 
```
./1_Get_LO_Portable.sh
```
starten. Es lädt die zurzeit aktuelle Version 7.6 herunter. Da sich die Download-Adressen bei neueren Versionen ändern, sehen Sie auf https://download.documentfoundation.org/libreoffice/stable nach, ob die Angaben im Script noch stimmen. Wenn nötig, ändern Sie die Versionsnummern im Konfigurationsbereich des Scripts. Das Script lädt die Dateien herunter und speichert Libre Office im Ordner „~/lwPDF/libreoffice“.

Anschließend verwenden Sie "2_Get_Python_Modules.sh" aus dem Ordner „install“. Eventuell müssen Sie darin Anpassungen im Konfigurationsabschnitt vornehmen, wenn sich die Python-Version von Libre Office ändert.

Das Script installiert zuerst PIP (Package Installer for Python) in Libre Office, über das sich weitere Module herunterladen lassen. Alle installierten Dateien liegen im Ordner "~/lwPDF/libreoffice/program/python-core-3.8.17".

## Beispielanwendungen ausprobieren
Für einen ersten Test verwenden Sie die Bash-Scripte.

**lwPDFServer.sh**: Das Script aktiviert sowohl Libre Office als Server als auch den Webserver. Die Webanwendung öffnet sich automatisch im Browser unter der Adresse "http://127.0.0.1:8080/". In der Web-Oberfläche wählen Sie ein Ausgabeformat, beispielsweise "PDF". Klicken Sie auf "Durchsuchen" und wählen Sie einen Datei zum Konvertieren aus. Danach klicken Sie auf "Datei herunterladen". PDF-Dateien werden gespeichert, danach zeigt der Browser sie an. Bei PDF-Dateien sind zusätzliche Optionen möglich, etwa die Vergabe eines Kennworts fürs Öffnen oder die Beschränkung auf eine bestimmte Seitenzahl.

Damit der Webserver von "lwPDFServer.sh" netzwerkweit erreichbar ist, ergänzen Sie im Bash-Script den Start von "webware serve" mit dem Parameter "-l" gefolgt von der IP-Nummer oder dem Namen des Servers. Lassen Sie "-b" weg, damit sich die Webseite nicht automatisch im Browser öffnet.

**lwPDFKonverter.sh**: Damit wird das wird das Python-Script "lwPDFConverter.py" gestartet. Es überwacht den Ordner "files/in" im Installationsverzeichnis. Sobald neue Dateien in diesem Ordner auftauchen, konvertiert lwPDFKonverter sie automatisch und legt die PDF-Dateien im Ordner "files/out" ab. Wenn Sie die Ordner über Samba im Netzwerk freigeben, können auch Nutzer anderer PCs den Dienst von "lwPDFConverter.py" nutzen.

## Zusätzliche Beispiele für Webware
Die Webanwendung "lwPDFServer" enthält zwei weitere Funktionen, die Sie über die Links auf der Webseite aufrufen. "Suche in ODT-Dateien" ("search.psp") führt zu einem Formular, in das Sie einen Ordner mit Writer-Dateien und darunter einen Suchbegriff eintragen. Nach einem Klick auf "Senden" liefert das Script eine Liste aller Dateien, in denen der Begriff vorkommt, sowie den Kontext um den Begriff herum. Unterverzeichnisse werden berücksichtigt.

Der Link "Wetterdaten abrufen" öffnet "weather.psp". Die Seite zeigt Wetterdaten aus der Calc-Datei "~/lwPDF/lwPDF/MyContext/data/Wetter.ods" als Tabelle und darunter ein Diagramm mit dem mittleren Temperaturverlauf. Per Klick auf "Wetterdaten abholen" lädt das Script aktuelle Daten über http://api.openweathermap.org herunter. Damit das funktioniert, benötigen Sie einen kostenlosen API-Key, den Sie nach der Anmeldung bei https://openweathermap.org erhalten. Tippen Sie den Schlüssel im Konfigurationsabschnitt von "weather.psp" hinter "API_key" ein. Hinter "Standort" geben Sie den Ort an, für den Sie die Wetterdaten abrufen wollen.





