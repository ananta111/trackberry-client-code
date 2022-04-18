from numbers import Number

import time
import serial
import numpy as np
import matplotlib.pyplot as plt
import requests
import json

N = 1000  # number of samples to collect
i=0
x=np.zeros(N)
y=np.zeros(N)
i=0
arduino = serial.Serial(port='COM7', baudrate=9600, timeout=.1)
arduino.close()
arduino.open()


def gpSend(latitude, longitude):
    url = "https://trackberry-server.herokuapp.com/markers"
    data = {"type": "Feature",
            "geometry": {"type": "Point", "coordinates": [latitude, longitude]},
            "properties": {}
            }
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    res = requests.post(url, json=data)
    print (res)


def lat(deg, min):
    return deg + min/60
def long(deg, min):
    return deg + min/60



while 1:
    try:
        data = arduino.readline()
        if data:
            print(data)
            tokens = data.decode('ISO-8859-1').split(',')

            if (tokens[0][0] == "L"):
                tokens[1] = tokens[1].strip()
                tokens[3] = tokens[3].strip()
                latdeg = tokens[1][:2]
                latmin = tokens[1][2:]
                NS = tokens[2]
                EW = tokens[4]
                #print(tokens)
                #print(latdeg)
                #print(latmin)
                if(len(tokens[3]) == 10):
                    longdeg = tokens[3][:3]
                    longmin = tokens[3][3:]
                    #print(longdeg)
                    #print(longmin)
                elif(len(tokens[3])==9):
                    longdeg = tokens[3][:2]
                    longmin = tokens[3][2:]

                    #print(longdeg)
                    #print(longmin)
                else:
                    longdeg = tokens[3][:2]
                    longmin = tokens[3][2:]
                #print(tokens[4])
                sendLat = (lat(float(latdeg), float(latmin)))
                sendLong = (long(float(longdeg), float(longmin)))
                #print(type(NS))
                if ("S" in NS):
                    sendLat = -1*sendLat
                elif("W" in EW):
                    sendLong = -1*sendLong
                print(sendLat)
                print(sendLong)
                print(gpSend(sendLong, sendLat))
                arduino.close()
                time.sleep(60)
                arduino.open()
    except:
        time.sleep(15)








