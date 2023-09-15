import json
import time

import numpy as np
import paho.mqtt.client as mqtt


def calc_bearing(a_lat: float, a_lon: float, b_lat: float, b_lon: float) -> float:
    """
    Calculate the bearing between two points.

    https://towardsdatascience.com/calculating-the-bearing-between-two-geospatial-coordinates-66203f57e4b4

    """
    dL = b_lon - a_lon

    x = np.cos(b_lat)*np.sin(dL)
    y = np.cos(a_lat)*np.sin(b_lat) - np.sin(a_lat)*np.cos(b_lat)*np.cos(dL)

    bearing = np.arctan2(x, y)
    return np.rad2deg(bearing)


def on_connect(client: mqtt.Client, userdata, flags, rc: int):
    print(f"on_connect: {rc}")


def on_disconnect(client: mqtt.Client, userdata, rc: int):
    print(f"on_disconnect: {rc}")


def main():
    a_lat = 0
    a_lon = 0
    b_lat = 0
    b_lon = 0

    client = mqtt.Client("laptop")
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect

    client.connect("127.0.0.1")

    with open("position.txt", "r") as file:
        for line in file:
            lat = float(line.split("lat=")[1].split(",")[0])
            lon = float(line.split("lon=")[1].split(",")[0])
            hacc = int(line.split("hAcc=")[1].split(",")[0])
            vacc = int(line.split("vAcc=")[1].split(")")[0])

            b_lat = lat
            b_lon = lon

            bearing = calc_bearing(a_lat, a_lon, b_lat, b_lon)

            a_lat = b_lat
            a_lon = b_lon

            color = "red"
            solution = "3D"
            if hacc < 200 and vacc < 200:
                color = "orange"
                solution = "FLOAT"
            if hacc < 20 and vacc < 20:
                color = "green"
                solution = "FIXED"
            
            data = {
                "name": "rover",
                "lat": lat,
                "lon": lon,
                "bearing": bearing,
                "icon": "car",
                "iconColor": color,
                "label": f"{solution} hAcc={hacc}, vAcc={vacc}"
            }
            message = json.dumps(data)
            payload = message.encode("utf-8")
            client.publish("car-tracker", payload)
            time.sleep(0.2)
    
    client.disconnect()


if __name__ == "__main__":
    main()
