import geopandas as gpd
from pyproj import CRS
from shapely.geometry import Point


def main():
    # Create a GeoDataFrame object and add columns.
    geodf = gpd.GeoDataFrame()
    geodf["geometry"] = None
    geodf["hacc"] = None
    geodf["vacc"] = None

    # Set the coordinate reference system (CRS) to WGS84.
    geodf.crs = CRS.from_epsg(4326).to_wkt()

    # Read the accuracy values and write them into the geodataframe.
    i = 0
    with open("position.txt", "r") as file:
        for line in file:
            lat = float(line.split("lat=")[1].split(",")[0])
            lon = float(line.split("lon=")[1].split(",")[0])
            hacc = int(line.split("hAcc=")[1].split(",")[0])
            vacc = int(line.split("vAcc=")[1].split(")")[0])
            geodf.at[i, "geometry"] = Point(lon, lat)
            geodf.at[i, "hacc"] = hacc
            geodf.at[i, "vacc"] = vacc
            i += 1

    # Define the data type of the columns in order to avoid shape file
    # import error in Blender.
    geodf["hacc"] = geodf["hacc"].astype("Int64")
    geodf["vacc"] = geodf["vacc"].astype("Int64")
    # WGS84 -> Web Mercator.
    geodf = geodf.to_crs(epsg=3857)

    # Change the geometry so that it is possible to add material to the
    # data points in Blender.
    route = geodf.copy()
    route["geometry"] = route["geometry"].buffer(10)
    route.to_file("route.shp")


if __name__ == "__main__":
    main()
