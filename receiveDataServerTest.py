from flask import Flask, Response, request
import csv
import requests
import operator
import time
import datetime
import json

app = Flask(__name__)
#python receiveDataServerTest.py
@app.route("/")
def CSVtoServer():
	url = 'https://sigma-myth-229819.appspot.com/truckapi'
	driverUrl = 'https://sigma-myth-229819.appspot.com/driverApi'
	headers = { 'Content-Type': 'application/json' }

	with open('ITM_20190121.csv') as csv_file:
		csv_read = csv.reader(csv_file, delimiter=',')
		sortedCSV = sorted(csv_read, key=operator.itemgetter(7))
		counter = 0;

		for i in range(len(sortedCSV)):
			if sortedCSV[i][9] != 'NULL' and sortedCSV[i][8] != 'NULL' and sortedCSV[i][1] != 'NULL':
				driverDict = {"driverID": "12345", "lon": float(sortedCSV[i][9]), "lat": float(sortedCSV[i][8]) }
				tempDict = {"Longitude": float(sortedCSV[i][9]), "Latitude": float(sortedCSV[i][8]), "DeviceSerial": int(sortedCSV[i][1]), "MessageType": sortedCSV[i][3], "ReportType":sortedCSV[i][4]}
				response = requests.post(url, headers=headers, data=json.dumps(tempDict))
				if int(sortedCSV[i][1]) == 1084067241 and counter < 59:
					driverResponse = requests.post(driverUrl, headers=headers, data=json.dumps(driverDict))
				print(driverDict, driverResponse)
				print(tempDict, response)
				counter += 1;
				print(counter)			
				if(i + 1 != len(sortedCSV)):
			
					newStr = sortedCSV[i][7]
					newStr2 = sortedCSV[i+1][7]
					newStr = newStr[12:-4]
					newStr2 = newStr2[12:-4]
					ftr = [3600,60,1]
					x = sum([a*b for a,b in zip(ftr, map(int,newStr.split(':')))])
					x2 = sum([a*b for a,b in zip(ftr, map(int,newStr2.split(':')))])
					tempDiff = (x2-x) / 100
					print(tempDiff)
					time.sleep(tempDiff)

			
		return "Data Sent."
		
if __name__ == "__main__":
	app.run()