# -*- coding: utf-8 -*-
import sys
import uno, os, time
import unohelper
import requests
from time import strftime
from datetime import datetime
from com.sun.star.beans import PropertyValue
import configparser

### Konfiguration ###
# API-Key von openweathermap.org
#
config = configparser.ConfigParser()
config.read("lwPDF/API_KEY.ini")
API_key = config.get("config", "API_key")
Standort = config.get("config", "Standort")
# siehe weiter unten unter "Länge und Breite verwenden"
lat = config.get("config", "lat")
lon = config.get("config", "lon")
# Beispiele
#Standort = "Munich"
# oder Länge und Breite
# dafür URL in getWeather() anpassen
#lat="48.155709"
#lon="11.548687"
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

def getDOC(filename):
	pathname = os.getcwd() 
	psep=os.path.sep
	outpath = pathname + psep + 'out' + psep
	properties = UnoProps(Hidden=True)
	context = uno.getComponentContext()
	resolver = context.ServiceManager.createInstanceWithContext("com.sun.star.bridge.UnoUrlResolver", context)
	ctx = resolver.resolve("uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext")
	smgr = ctx.ServiceManager
	desktop = smgr.createInstanceWithContext("com.sun.star.frame.Desktop",ctx)
	cwd = unohelper.systemPathToFileUrl( os.getcwd() )
	#url = unohelper.absolutize(cwd, unohelper.systemPathToFileUrl(userfile))
	url=unohelper.absolutize(cwd, unohelper.systemPathToFileUrl(filename))
	doc = desktop.loadComponentFromURL( url , "_blank", 0, properties )
	return doc
	
def getWeather():
	API_anfrage_url = "http://api.openweathermap.org/data/2.5/weather?q="+Standort+",de&appid="+API_key+"&units=metric"
	#Länge und Breite verwenden
	#https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API key}
	#48.155709, 11.548687, München
	# lat="48.155709"
	# lon="11.548687"
	#Verwenden Sie dann diese Form der Abfrage
	#API_anfrage_url = "https://api.openweathermap.org/data/2.5/weather?lat="+ lat + "&lon=" + lon + "&appid=" + API_key +"&units=metric"
	wetterdaten_anfrage = requests.get(API_anfrage_url) 
	wetterdaten = wetterdaten_anfrage.json() 
	#Beispiel für die Rückgabe der Wetterdaten im Json-Format
	#weatherdata={'coord': {'lon': 11.5755, 'lat': 48.1374}, 'weather': [{'id': 804, 'main': 'Clouds', 'description': 'overcast clouds', 'icon': '04d'}], 'base': 'stations', 'main': {'temp': 298.99, 'feels_like': 299.22, 'temp_min': 298.47, 'temp_max': 299.67, 'pressure': 1016, 'humidity': 61}, 'visibility': 10000, 'wind': {'speed': 2.37, 'deg': 210, 'gust': 4.35}, 'clouds': {'all': 88}, 'dt': 1689696233, 'sys': {'type': 2, 'id': 2002112, 'country': 'DE', 'sunrise': 1689651108, 'sunset': 1689707254}, 'timezone': 7200, 'id': 2867714, 'name': 'Munich', 'cod': 200}
	#return weatherdata
	return wetterdaten

def writeCalc():
	from datetime import datetime as dt #python
	from com.sun.star.util import Date  #uno-api
	current_weather=[]
	psep=os.path.sep
	doc=getDOC(os.getcwd() + psep + "lwPDF" + psep + "MyContext" + psep + "data" + psep + "Wetter.ods")
	sheet = doc.Sheets.getByName("Wetter")
	for row in range(2, 200):
		value=sheet.getCellByPosition(0, row).getString()
		if value =='':
			break
	last_row = int(row)
	oLocale = uno.createUnoStruct("com.sun.star.lang.Locale")
	oLocale.Language = "de"
	oLocale.Country = "DE"
	# Bei Bedarf Nummern-Formate ermitteln
	#oNumberFormats = doc.NumberFormats
	#NumberFormatString = u'HH:MM:SS'
	#NumberFormatId = oNumberFormats.queryKey(NumberFormatString, oLocale, True)
	# Datum für Calc umrechnen
	# Es handelt sich um ein serielles Datum,
	# das am 30.12.1899 startet
	named_tuple = time.localtime() # get struct_time	
	oValue=sheet.getCellByPosition(0, last_row)
	uno_date = Date()
	#uno_date.Year, uno_date.Month, uno_date.Day = 2023, 5, 25
	uno_date.Year, uno_date.Month, uno_date.Day = dt.today().year, dt.today().month, dt.today().day
	py_date = dt(year=uno_date.Year, month=uno_date.Month, day=uno_date.Day)
	calc_zero = dt(1899, 12, 30)
	# siehe:
	# https://docs.python.org/3/library/datetime.html?highlight=toordinal#datetime.datetime.toordinal
	calc_date = py_date.toordinal() - calc_zero.toordinal()
	oValue.setValue(calc_date)
	oValue.NumberFormat=37 #Datum DD.MM.YY
	
	oValue=sheet.getCellByPosition(1, last_row)
	# Zeit für Calc umrechnen
	time_string = time.strftime("%H:%M:%S", named_tuple)
	(h, m, s) = time_string.split(':')
	my_time=(60*60*int(h) + 60*int(m) + int(s))/(24*60*60)
	oValue.setValue(my_time)
	oValue.NumberFormat=10061 #Zeit HH:MM:SS	
	#Wetterdaten abholen 
	weather_data=getWeather()
	temp_min=("%.1f" % weather_data['main']['temp_min']).replace(".",",")
	current_weather.append(temp_min)
	print ('Temperatur min.: ' + temp_min)
	temp_max=("%.1f" % weather_data['main']['temp_max']).replace(".",",")
	current_weather.append(temp_max)
	print ('Temperatur max.: ' + temp_max)
	temp=("%.1f" % weather_data['main']['temp']).replace(".",",")
	current_weather.append(temp)
	print ('Temperatur: ' + temp)
	current_weather.append(weather_data['main']['humidity'])
	print ('Luftfeuchtigkeit (%): {}'.format(weather_data['main']['humidity']))
	current_weather.append(weather_data['wind']['speed'])
	print ('Windgeschwindigkeit (M/S): {}'.format(weather_data['wind']['speed']))
	timezone = int(weather_data['timezone'])
	sunrise_utc = int(weather_data['sys']['sunrise'])
	sunrise_local = datetime.utcfromtimestamp(sunrise_utc + timezone).strftime('%H:%M:%S')
	sunset_utc = int(weather_data['sys']['sunset'])
	sunset_local = datetime.utcfromtimestamp(sunset_utc + timezone).strftime('%H:%M:%S')
	print('Sonnenaufgang: {}'.format(sunrise_local))
	print('Sonnenuntergang: {}'.format(sunset_local))
	current_weather.append(sunrise_local)
	current_weather.append(sunset_local)
	col=2
	for data in current_weather:
		oValue=sheet.getCellByPosition(col, last_row)
		oValue.setString(data)
		col+=1
	# Datei speichern
	doc.store()
	# Datei freigeben
	doc.dispose()
	
# Wetterdaten aus Calc-Tabelle lesen
def readCalc():
	psep=os.path.sep
	doc=getDOC(os.getcwd() + psep + "lwPDF" + psep + "MyContext" + psep + "data" + psep + "Wetter.ods")
	sheet = doc.Sheets.getByName("Wetter")
	for row in range(2, 200):
		value=sheet.getCellByPosition(0, row).getString()
		if value =='':
			break

		for col in range(0,8):
			value=sheet.getCellByPosition(col, row).getString()
			print ("Cell: " + value)
			
	print(row)
	doc.dispose()

# Hauptprogramm startet hier
if API_key == "":
	print("Fehler: Konfigurieren Sie die Variable API_key in der Datei lwPDF/API_KEY.ini.")
else:
	print ("Hole Wetterdaten...")
	writeCalc()

