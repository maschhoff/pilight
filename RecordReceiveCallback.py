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
	protocol_contact_list = {'GS-iwds07'}
	item_list = {38586: 'Kuechenfenster', 153:'Temp1_String', 85: 'Temp2_String'}
	


	#if code["protocol"] == "alecto_ws1700" or code["protocol"] == "teknihall":
	if code["protocol"] in protocol_weather_list:
		id=code["message"]["id"]
		temp=code["message"]["temperature"]
		humidity=code["message"]["humidity"]
		if id in item_list:
			sendToOpenHAB(item_list[id],str(round(temp,9)))
			sendToOpenHAB(item_list[id]+'_Humidity',str(round(humidity,9)))
	if code["protocol"] in protocol_contact_list:
		id=code["message"]["unit"]
		data=code["message"]["state"]
		if id in item_list:
			sendToOpenHAB(item_list[id],data)
#-------------------  Aktions  ------------------------------------------
# Senderoutine    siehe https://manual.pilight.org/development/api.html
def sendToOpenHAB(item,data):
	logging.info("SEND TO OPENHAB - ITEM: "+item+" DATA: "+data)
	# OpenHAB API aufrufen
	url = "http://10.10.10.4:8080/rest/items/"+item
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
	except:
		e=sys.exec_info()[0]
		logging.warn("Exception: " % e)
