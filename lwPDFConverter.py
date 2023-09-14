# -*- coding: utf-8 -*-
# Libre-Office-Dateien automatisch in das PDF-Format umwandeln.
# Das Verzeichnis "files/in" wird auf neue Dateien überwacht.
# Die PDF-Dateien werden in "files/out" gespeichert.
#
# Python-Module importieren
import sys
import uno, os, time
import unohelper 
from time import strftime
from com.sun.star.beans import PropertyValue

### Konfiguration ###
# Dateien im Eingangsordner nach der Konvertierung automatisch löschen
# removeFile="yes"
removeFile="no"
# PDF-Dateinamen mit Datum und Uhrzeit erstellen
useDate="yes"
### Konfiguration Ende ###

oServiceManager = False
ctx = uno.getComponentContext()

#Properties für StarOffice-Objekte
def UnoProps(**args):
	props = []
	for key in args:
		prop = PropertyValue()
		prop.Name = key
		prop.Value = args[key]
		props.append(prop)
	return tuple(props)

def executeScript( ctx, script, args ):
	masterScriptProvider = ctx.ServiceManager.createInstanceWithContext("com.sun.star.script.provider.MasterScriptProviderFactory", ctx )
	scriptProvider = masterScriptProvider.createScriptProvider( " " )
	myScript = scriptProvider.getScript( script )
	myScript.invoke(args,(),()) 

def ConvertToPDF(userfile):
	print ('Exportiere...'+ userfile)
	pathname = os.getcwd() 
	psep=os.path.sep
	outpath = pathname + psep + "files" + psep + "out" + psep

	if os.path.isfile(userfile):
		(up_path, up_file) = os.path.split(userfile)	 

		export_format = 'writer_pdf_Export'

		if useDate == 'yes':
			url_save = uno.systemPathToFileUrl(outpath + up_file+"-"+strftime("%Y-%m-%d-%H-%M-%S")+'.pdf')
		else:
			url_save = uno.systemPathToFileUrl(outpath + up_file+'.pdf')
		
		properties = UnoProps(Hidden=True)
		context = uno.getComponentContext()
		resolver = context.ServiceManager.createInstanceWithContext("com.sun.star.bridge.UnoUrlResolver", context)
		ctx = resolver.resolve("uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext")
		smgr = ctx.ServiceManager
		desktop = smgr.createInstanceWithContext("com.sun.star.frame.Desktop",ctx)
		cwd = unohelper.systemPathToFileUrl( os.getcwd() )
		url = unohelper.absolutize(cwd, unohelper.systemPathToFileUrl(userfile))
		doc = desktop.loadComponentFromURL( url , "_blank", 0, properties )
		outproperties = UnoProps(FilterName=export_format, Hidden=True, Overwrite=True)

		try:
			doc.storeToURL(url_save, tuple(outproperties))
		except:
			print ("Fehler beim Schreiben:")
		doc.dispose()
		if removeFile=='yes':
			print ('Entferne: ' + userfile)
			os.remove(userfile)
	else:
		print ("Datei nicht gefunden")

# Das Hauptprogramm startet hier
print ("lwPDFKonverter gestartet.")
print ("Warte auf Dateien...")
pathname = os.getcwd() 
psep=os.path.sep
path_to_watch = pathname + psep + "files" + psep + "in" + psep

#Schleife zur Verzeichnisüberwachung
before = dict ([(f, None) for f in os.listdir (path_to_watch)])
while 1:
	time.sleep (10)
	after = dict ([(f, None) for f in os.listdir (path_to_watch)])
	added = [f for f in after if not f in before]
	removed = [f for f in before if not f in after]
	if added:
		print ("Hinzugefügt: ", ", ".join (added))
		myFile="".join (added)
		myFile=path_to_watch+ myFile
		for v in added:
			myFile=path_to_watch+ v
			ConvertToPDF(myFile)

	if removed: print ("Entfernt: ", ", ".join (removed))
	before = after
