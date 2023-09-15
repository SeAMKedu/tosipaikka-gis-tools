import folium
from folium.plugins import HeatMap

FILENAME = "position.txt"
LOCATION_LAT = 62.807772
LOCATION_LON = 23.507498


def main():
    lats = []
    lons = []

    with open(FILENAME, "r") as file:
        for line in file:
            lat = float(line.split("lat=")[1].split(",")[0])
            lon = float(line.split("lon=")[1].split(",")[0])
            lats.append(lat)
            lons.append(lon)

    locations = list(zip(lats, lons))

    m = folium.Map(
        location=[LOCATION_LAT, LOCATION_LON],
        tiles="OpenStreetMap",
        zoom_start=10
    )

    HeatMap(data=locations).add_to(m)

    m.save("index.html")

if __name__ == "__main__":
    main()
