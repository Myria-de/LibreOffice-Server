# LibreOffice im Servermodus nutzen
Der Server-Modus von Libre Office bietet Schnittstellen, über die sich die Funktionen des Büropakets per Script nutzen lassen. Mit einem Webserver kann der Zugriff auch über das Netzwerk erfolgen.
## Libre Office und Python-Module einrichten
**Für Windows:** Laden Sie das Archiv [
PC-WELT PDF-Server](https://www.myria.de/?sdm_process_download=1&download_id=323748) herunter. LibreOffice-Portable und die Python-Module sind bereits enthalten. Die Python-Scripte sind mit denen für Linux weitestgehend identisch. Entpacken Sie das Archiv in den Ordner "C:\pcwPDF". Die PSP-Dateien aus dem Ordner "pcwPDF/MyContext/" müssen bei Änderungen mit der Codierung "ANSI" gespeichert werden und nicht als "UTF-8". Zum Start der Anwendungen gibt es entsprechende Batch-Dateien.

**Für Linux:** Laden Sie das Archiv über https://github.com/Myria-de/LibreOffice-Server/archive/refs/tags/v2.4.tar.gz herunter. Entpacken/kopieren Sie alle Dateien in Ihr Home-Verzeichnis, beispielsweise in den Ordner "~/lwPDF".

Die Installation von Libre Office erfolgt unter Linux über ein Bash-Script, das Sie im Terminal im Ordner "~/lwPDF/install" mit 
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

**Bitte beachten Sie:** Der Webserver Waitress eignet sich für das lokale Netzwerk, genügt aber keinen höheren Sicherheitsansprüchen. Über das Internet sollten Sie diesen Dienst daher nicht bereitstellen. Wer das plant, richtet einen Apache- oder Nginx-Webserver als Reverse-Proxy ein (siehe https://webwareforpython.github.io/w4py3/deploy.html).

![402_02_LO_Konverter](https://github.com/Myria-de/LibreOffice-Server/assets/6861591/c54ab373-2a48-4be2-8421-b8a7c28591c6)

**lwPDFKonverter.sh**: Damit wird das wird das Python-Script "lwPDFConverter.py" gestartet. Es überwacht den Ordner "files/in" im Installationsverzeichnis. Sobald neue Dateien in diesem Ordner auftauchen, konvertiert lwPDFKonverter sie automatisch und legt die PDF-Dateien im Ordner "files/out" ab. Wenn Sie die Ordner über Samba im Netzwerk freigeben, können auch Nutzer anderer PCs den Dienst von "lwPDFConverter.py" nutzen.

Im Terminal gestartet, lässt sich die Ausführung mit Strg-C abbgrechen. Libre-Office-Server sollte damit ebenfalls beendet werden. Wenn nicht, lässt sich das Program über "LO_shutdown.sh" beenden.

Als Demo und zum Vergleich dient das Script **"convert-to-cli.sh"**. Es verwendet im Terminal Optionen für die Kommandozeile, um eine Datei direkt mit Libre Office (nicht im Server-Modus) zu konvertieren. Rufen Sie es mit 
```
./convert-to-cli.sh Dokument.odt
```
auf. 

## Zusätzliche Beispiele für Webware
Die Webanwendung "lwPDFServer" enthält zwei weitere Funktionen, die Sie über die Links auf der Webseite aufrufen. "Suche in ODT-Dateien" ("search.psp") führt zu einem Formular, in das Sie einen Ordner mit Writer-Dateien und darunter einen Suchbegriff eintragen. Nach einem Klick auf "Senden" liefert das Script eine Liste aller Dateien, in denen der Begriff vorkommt, sowie den Kontext um den Begriff herum. Unterverzeichnisse werden berücksichtigt.

Der Link "Wetterdaten abrufen" öffnet "weather.psp". Die Seite zeigt Wetterdaten aus der Calc-Datei "~/lwPDF/lwPDF/MyContext/data/Wetter.ods" als Tabelle und darunter ein Diagramm mit dem mittleren Temperaturverlauf. Per Klick auf "Wetterdaten abholen" lädt das Script aktuelle Daten über http://api.openweathermap.org herunter. Damit das funktioniert, benötigen Sie einen kostenlosen API-Key, den Sie nach der Anmeldung bei https://openweathermap.org erhalten. Tippen Sie den Schlüssel im Konfigurationsabschnitt von "weather.psp" hinter "API_key" ein. Hinter "Standort" geben Sie den Ort an, für den Sie die Wetterdaten abrufen wollen.

**lwGetWeather.sh** ist für einen Cronjob gedacht, der regelmäßig die Wetterdaten abholt und in die Calc-Tabelle schreibt. Tragen Sie den API-Key in "lwGetWeather.py" ein.

![402_06_Wetterdaten](https://github.com/Myria-de/LibreOffice-Server/assets/6861591/c3a8c6b7-07a6-416d-81ac-0038ddcb3919)

## Programme als Dienst starten
Bei regelmäßiger Nutzung ist es bequemer, Libre Office und die Scripte über einen Systemd-Dienst zu starten. Vorbereitete Dateien finden Sie im Ordner "Services".

Die Datei "soffice.service" startet Libre Office. Der Inhalt muss für das System angepasst werden. Hinter "User=" und "Group=" gehören Benutzername und Gruppe des Linux-Kontos, das den Dienst starten soll. Administrative Rechte sind nicht erforderlich und aus Sicherheitsgründen auch nicht erwünscht. Die Variable "$HOME" verweist in allen Dienste auf das Home-Verzeichnis dieses Benutzers. Passen Sie die Pfadangaben dahinter an, wenn Sie einen anderen Ordner als "lwPDF" verwenden.

Mit der Zeile
```
ExecStart=/usr/bin/bash -c "exec $HOME/lwPDF/libreoffice/program/soffice --headless --nologo --nodefault --nofirststartwizard --accept='socket,host=localhost,port=2002;urp;'"
```
wird Libre Office gestartet.

Kopieren Sie die angepasste Datei in den Ordner "/etc/systemd/system". Aktivieren und starten Sie den Dienst mit 
```
sudo systemctl enable soffice.service
sudo systemctl start soffice.service
```
Spätere Änderungen in der Datei teilen Sie dem System über 
```
sudo systemctl daemon-reload
```
mit.

Die Datei "webware.service" ist ähnlich aufgebaut und muss vor der Verwendung ebenfalls angepasst, aktiviert und gestartet werden. Der Dienst startet das Script mit
```
ExecStart=/bin/bash -c '${HOME}/lwPDF/lwPDFServer.sh'
```
In der Datei "~/lwPDF/lwPDFServer.sh" passen Sie den Aufruf von Webware für den Dienst an. Die Befehlszeile lautet
```
exec $SCRIPTPATH/libreoffice/program/python $SCRIPTPATH/libreoffice/program/$PYVER/bin/webware serve -l [host] --prod
```
Den Platzhalter "[host]" ersetzen Sie durch den Namen des Servers oder seine IP-Nummer. Ohne diese Angabe ist der Server nur über "http://127.0.0.1:8080/" (localhost) erreichbar.

**Bitte beachten Sie:** Webware speichert die Scripte in einem Cache. Wenn Sie eine PSP-Datei anpassen, starten Sie den Dienst mit
```
sudo systemctl restart webware.service
```
neu.

Der Dienst "lwPDFKonverter.service" enthält für den Programmstart die Zeile
```
ExecStart=/bin/bash -c "cd $HOME/lwPDF; exec libreoffice/program/python lwPDFConverter.py"
```
Es ist notwendig, zuerst in das Arbeitsverzeichnis "lwPDF" zu wechseln, damit das Python-Script die Ordner "in" und "out" findet.

**Unter Windows:** 
Verwenden Sie die Aufgabenplanung zum Start der Anwendungen. Erstellen Sie die Aufgabe in einer Eingabeaufforderung.

**pcwPDF_Server:**
```
schtasks /create /tn "RunPDFServer" /sc onstart /ru system /tr "cmd.exe /c C:\pcwPDF\pcwPDF_Server.bat"
```
**pcwPDFKonverter:**
```
schtasks /create /tn "RunPDFKonverter" /sc onstart /ru system /tr "cmd.exe /c C:\pcwPDF\pcwPDFKonverter.bat"
```
**pcwGetWeatherData:**
```
schtasks /create /tn "RunGetWeather" /tr "cmd.exe /c C:\pcwPDF\pcwGetWeatherData.bat" /sc daily /sd 01/01/2023 /st 12:00
```
