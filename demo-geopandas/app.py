import folium
import geopandas as gpd
from geopandas.tools import geocode
from pyproj import CRS

GAS_STATIONS = [
    {
        "addr": "Ruukintie 177, 60200 Seinäjoki, Finland",
        "corp": "ABC",
        "95E10": 2.106, "98E": 2.200, "Di": 2.148
    },
    {
        "addr": "Hyllykalliontie 1, 60510 Seinäjoki, Finland",
        "corp": "St1",
        "95E10": 2.149, "98E": 2.219, "Di": 2.379
    },
    {
        "addr": "Vapaudentie 73, 60100 Seinäjoki, Finland",
        "corp": "Neste",
        "95E10": 2.119, "98E": 2.219, "Di": 2.249
    },
    {
        "addr": "Valtionkatu 7, 60100 Seinäjoki, Finland",
        "corp": "Shell",
        "95E10": 2.121, "98E": 2.231, "Di": 2.156
    },
    {
        "addr": "Verkatehtaankatu 13, 60100 Seinäjoki, Finland",
        "corp": "ABC",
        "95E10": 2.108, "98E": 2.207, "Di": 2.183
    },
    {
        "addr": "Vapaudentie 25, 60100 Seinäjoki, Finland",
        "corp": "Neste",
        "95E10": 2.134, "98E": 2.234, "Di": 2.269
    },
    {
        "addr": "Kasperinviita 15, 60150 Seinäjoki, Finland",
        "corp": "Neste",
        "95E10": 2.114, "98E": 2.204, "Di": 2.244
    },
    {
        "addr": "Tapiolantie 10, 60150 Seinäjoki, Finland",
        "corp": "St1",
        "95E10": 2.114, "98E": 2.204, "Di": 2.244
    },
    {
        "addr": "Kytöpolku 2, 60320 Seinäjoki, Finland",
        "corp": "ABC",
        "95E10": 2.149, "98E": 2.249, "Di": 2.289
    },
    {
        "addr": "Bullerintie 2, 60200 Seinäjoki, Finland",
        "corp": "ABC",
        "95E10": 2.149, "98E": 2.249, "Di": 2.289
    },
    {
        "addr": "Kivistöntie 30, 60100 Seinäjoki, Finland",
        "corp": "ABC",
        "95E10": 2.066, "98E": 2.151, "Di": 2.095
    },
    {
        "addr": "Hyllykalliontie 2, 60510 Seinäjoki, Finland",
        "corp": "ABC",
        "95E10": 2.075, "98E": 2.168, "Di": 2.104
    },
    {
        "addr": "Päivölänkatu 39, 60120 Seinäjoki, Finland",
        "corp": "St1",
        "95E10": 2.056, "98E": 2.146, "Di": 2.083
    },
]

LOCATION_LAT = 62.778323
LOCATION_LON = 22.848453


def main():
    # Initialize a geodataframe.
    geo1 = gpd.GeoDataFrame()
    geo1["addr"] = None
    geo1["corp"] = None
    geo1["95E10"] = None
    geo1["98E"] = None
    geo1["Di"] = None

    # Insert data into the geodataframe.
    for i, station in enumerate(GAS_STATIONS):
        geo1.at[i, "addr"] = station["addr"]
        geo1.at[i, "corp"] = station["corp"]
        geo1.at[i, "95E10"] = station["95E10"]
        geo1.at[i, "98E"] = station["98E"]
        geo1.at[i, "Di"] = station["Di"]

    # Fetch the locations of the gas stations.
    geo2 = geocode(geo1["addr"], provider="nominatim", user_agent="demo", timeout=8)
    geo2.crs = CRS.from_epsg(4326).to_wkt()

    # Combine geodataframes.
    geodf = geo2.join(geo1)

    # Create a map instance.
    m = folium.Map(
        location=[LOCATION_LAT, LOCATION_LON],
        zoom_start=12,
        control_scale=True
    )

    # Add markers to the map instance.
    for _, row in geodf.iterrows():
        point = row["geometry"]
        addr = row["addr"]
        street = addr.split(",")[0]
        corp = row["corp"]
        tooltip = f"<b>{corp}</b> {addr}"
        p0 = f"{corp}, {street}<br>"
        p1 = f"<br>95E10:&nbsp;{row['95E10']}"
        p2 = f"<br>98E:&emsp;&nbsp;{row['98E']}"
        p3 = f"<br>Di:&emsp;&ensp;&nbsp;{row['Di']}"
        iframe = folium.IFrame(f"{p0}{p1}{p2}{p3}")
        popup = folium.Popup(iframe, min_width=200, max_width=200) 
        if corp == "ABC":
            icon = folium.Icon(color="orange", icon="info-sign")
        elif corp == "Neste":
            icon = folium.Icon(color="blue", icon="info-sign")
        elif corp == "Shell":
            icon = folium.Icon(color="green", icon="info-sign")
        elif corp == "St1":
            icon = folium.Icon(color="red", icon="info-sign")
        folium.Marker(
            location=[point.y, point.x], icon=icon, popup=popup, tooltip=tooltip
        ).add_to(m)

    m.save("index.html")


if __name__ == "__main__":
    main()
