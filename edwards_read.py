#!/usr/bin/env python3

import time
import datetime

import edwardsserial

# InfluxDB server
import configparser
import os

dir_path = os.path.dirname(os.path.abspath(__file__))

config = configparser.ConfigParser()
config.read(os.path.join(dir_path, 'influxdb.ini'))

token = config['Influx']['Token']
org = config['Influx']['Org']
url = config['Influx']['URL']
bucket = config['Influx']['Bucket']

port = config['Edwards']['Port']

import influxdb_client, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

write_client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)

write_api = write_client.write_api(write_options=SYNCHRONOUS)

def init():
    global g
    try: 
        g = edwardsserial.TIC(port)   
    except (ConnectionError, ConnectionRefusedError):
        print("Could not connect to remote target. Is the device connected?")


def read_pressure(g, chan):
    if chan not in ['1', '2', '3']:
        print("Wrong channel")
        return
    
    try:
        if chan == '1':
            p = g.gauge1.pressure
            #u = g.gauge1.unit
        elif chan == '2':
            p = g.gauge2.pressure
            #u = g.gauge2.unit
        elif chan == '3':
            p = g.gauge3.pressure
            #u = g.gauge3.unit
        return p
    except (ConnectionError, ConnectionRefusedError):
        print("Could not connect to remote target. Is the device connected?")

def write_influx(p1, sensor, time):
    '''
    p1 - float. Pressure value in mbar.
    sensor - string. p_1, p_2
    time - timestamp.
    '''
    point = (Point("pressure")
             .tag("unit", "mbar")
             .field(sensor, float(p1))
             .time(time)
            )

    write_api.write(bucket=bucket, org="Unipg", record=point)


def main():
    global g

    n = datetime.datetime.now(datetime.timezone.utc)

    current_time = n.isoformat()

    try:
        p_1 = float(read_pressure(g, '1')) # Pascal. To mbar divide by 100.
    except:
        # Gauge not connected. returns None and rises exception.
        pass
    else:
        write_influx(p_1/100, 'p_1', current_time)

    try:
        p_2 = float(read_pressure(g, '2'))
    except:
        pass
    else:
        write_influx(p_2/100, 'p_2', current_time)

    try:
        p_3 = float(read_pressure(g, '3'))
    except:
        pass
    else:
        write_influx(p_3/100, 'p_3', current_time)

    #print(current_time + "\t{:.2f}\t{:.2f}\t{:.2f}".format(p_1, p_2, p_3))


if __name__ == "__main__":
    init()
    main()

