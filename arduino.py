from numbers import Number

import time
import serial
import requests
import random
import json

from IOUtils import *

def setup():
    arduino = serial.Serial(port='COM7', baudrate=9600, timeout=.1)
    arduino.close()
    arduino.open()
    return arduino


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


def collect_from_arduino(sample_rate=3):
    arduino = setup()
    input_file_process = ProcessFile("output.txt")
    while 1:
        try:
            data = arduino.readline()
            if not data:
                break
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
                    # print(tokens)
                    # print(latdeg)
                    # print(latmin)
                    if (len(tokens[3]) == 10):
                        longdeg = tokens[3][:3]
                        longmin = tokens[3][3:]
                        # print(longdeg)
                        # print(longmin)
                    elif (len(tokens[3]) == 9):
                        longdeg = tokens[3][:2]
                        longmin = tokens[3][2:]

                        # print(longdeg)
                        # print(longmin)
                    else:
                        longdeg = tokens[3][:2]
                        longmin = tokens[3][2:]
                    # print(tokens[4])
                    sendLat = (lat(float(latdeg), float(latmin)))
                    sendLong = (long(float(longdeg), float(longmin)))
                    # print(type(NS))
                    if ("S" in NS):
                        sendLat = -1 * sendLat
                    elif ("W" in EW):
                        sendLong = -1 * sendLong
                    print(sendLat)
                    print(sendLong)

                    # g = Geometry(sendLat, sendLong)
                    g = Geometry(88.4, -99.7)
                    input_file_process.add_geometry_to_file(g)
                    print(gpSend(sendLong, sendLat))
                    arduino.close()
                    time.sleep(60)
                    arduino.open()
        except:
            time.sleep(sample_rate)
    input_file_process.close_file()


def test_collection(samples=44):
    test_process = ProcessFile("test_output.txt")
    for i in range(samples):
        latitude, longitude = -0.118092, 51.509865
        test_g = Geometry(latitude, longitude)
        test_process.add_geometry_to_file(test_g)


def send_to_db_from_file(input_file):
    output_file_process = ProcessFile(input_file, write=False)
    coordinates_list = output_file_process.get_geometry_from_file(input_file)
    print (len(coordinates_list))
    if not coordinates_list:
        raise Exception("empty file")
    for g in coordinates_list:
        latitude, longitude = g.get_latlng()
        gpSend(latitude, longitude)
        print ("seending to database", latitude, longitude)
    output_file_process.close_file()


def main(test=False):
    if test:
        test_collection()
        send_to_db_from_file("test_output.txt")
    else:
        collect_from_arduino()
        send_to_db_from_file("output.txt")


if __name__ == "__main__":
    main(test=True)
















