# Programm von  https://github.com/DavidLP/pilight
# Auf Basis von TxRx.py von Detlev Aschhoff 2017 

# Voraussetzung pip install pilight und pip install requests

#import json
import requests
import pprint
import time
import logging
import sys
from pilight import pilight	# pip3 install pilight -- Socket auf Pi

def auswertung(code):		# was passiert mit code	
#	print(code)
#-------------------   Rules  ------------------------------------------
# Empfang json Format

	protocol_weather_list = {'alecto_ws1700','teknihall'}
	protocol_contact_list = {'GS-iwds07','arctech_screen_old'}
	protocol_bell_list = {'ev1527'}
	item_list = {17479:'Wohnzimmerfenster_rechts', 
				10198:'Wohnzimmerfenster_links',	
				23302:'Kellertuer',	
				41434:'Wintergartenfenster', 
				474:'Schlafzimmerfenster', 
				38586: 'Kuechenfenster', 
				139:'Temp1_String', 
				180: 'Temp2_String', 
				800581:'Bell_String',
				30164: 'Badezimmerfenster',
				26324: 'Tuer',
				2:'Bewegung_x',
				15:'Bewegung_y'}
	


	#if code["protocol"] == "alecto_ws1700" or code["protocol"] == "teknihall":
	if code["protocol"] == "teknihall":
		id=code["message"]["id"]
		temp=code["message"]["temperature"]
		humidity=code["message"]["humidity"]
		sendToOpenHAB("Temp1_String",str(temp))
		sendToOpenHAB("Temp1_String_Humidity",str(round(humidity,9)))

	if code["protocol"] == "alecto_ws1700":
		id=code["message"]["id"]
		temp=code["message"]["temperature"]
		humidity=code["message"]["humidity"]
		
		logging.debug('Alecto INFO:\n ID:'+str(id)+'\n HUM: '+str(humidity)+'\n TEMP: '+str(temp))

		sendToOpenHAB('Temp2_String',str(round(temp,9)))
		sendToOpenHAB('Temp2_String_Humidity',str(round(humidity,9)))
	
	if code["protocol"] in protocol_contact_list:
		id=code["message"]["unit"]
		data=code["message"]["state"]
		if id in item_list:
			sendToOpenHAB(item_list[id],data)
	if code["protocol"] in protocol_bell_list:
		id=code["message"]["unitcode"]
		data=code["message"]["state"]
		if id in item_list:
			sendToOpenHAB(item_list[id],data)
#-------------------  Aktions  ------------------------------------------
# Senderoutine    siehe https://manual.pilight.org/development/api.html
def sendToOpenHAB(item,data):
	logging.info("SEND TO OPENHAB - ITEM: "+item+" DATA: "+data)
	# OpenHAB API aufrufen
	url = "http://192.168.0.4:8080/rest/items/"+item
	#data = str(round(temp,9))
	#data_json = json.dumps(data) # bei json data={"jsondata"} und als response data=data_json
	headers = {'Content-type': 'text/plain'}
	response = requests.post(url, data=data, headers=headers) 
	#pprint.pprint(response.json())
def run():
       logging.basicConfig(filename='piRecReci.log',level=logging.DEBUG)
       logging.info("Starte Pilight Pilight Recorder...")
       pilight_client = pilight.Client(host='localhost',port=5000)
       pilight_client.set_callback(auswertung)
       pilight_client.start()

        #Laufe endlos
       while 1:
               time.sleep(1)


#def alarm():
#		data = {"protocol": ["quigg_gt7000"],
#		"id": 2068,
#		"unit": 0,
#		"state": "on"}
#		pilight_client.send_code(data)
#		
#-------------------  Init  --------------------------------------------
if __name__ == '__main__':
	try:
		run()
	except Exception as e:
		logging.warn("Exception: "+repr(e))
		exit()
