import contextily as cx
import geopandas as gpd
import matplotlib.pyplot as plt
import pyproj
from shapely.geometry import Point

MAPFILE = "kuortane.tif"
# Boundaries of the map area in Spherical Mercator CRS (EPSG:3857)
NORTH = 9054787.88410333
WEST = 2614449.5607708204
SOUTH = 9051864.665976496
EAST = 2618011.7844762052


def read_data(filename: str) -> gpd.GeoDataFrame:
    """
    Return a GeoDataFrame object that contains accuracy values.

    :param str filename: Name of the datafile.
    :returns: DataFrame with 'geometry', 'hAcc', and 'vAcc' columns.
    :rtype: GeoDataFrame.

    """
    # Create an empty GeoDataFrame object.
    geodf = gpd.GeoDataFrame()
    # Add new columns to the GeoDataFrame.
    geodf["geometry"] = None
    geodf["hAcc"] = None
    geodf["vAcc"] = None
    # Set the coordinate reference system (CRS) to WGS84.
    geodf.crs = pyproj.CRS.from_epsg(4326).to_wkt()
    
    # Read horizontal and vertical accuracy values from the file.
    i = 0
    with open(f"{filename}.txt", "r") as file:
        for line in file:
            # Latitude and longitude.
            lat = float(line.split("lat=")[1].split(",")[0])
            lon = float(line.split("lon=")[1].split(",")[0])
            # Horizontal and vertical accuracy.
            hacc = int(line.split("hAcc=")[1].split(",")[0])
            vacc = int(line.split("vAcc=")[1].split(")")[0])
            # Insert to geodataframe.
            geodf.at[i, "geometry"] = Point(lon, lat)
            geodf.at[i, "hAcc"] = hacc
            geodf.at[i, "vAcc"] = vacc
            i += 1
    return geodf


def plot_data(data: gpd.GeoDataFrame, service: str):
    """
    Plot the horizontal and vertical accuracy of the GNSS receiver.

    :param GeoDataFrame data: Data to be plotted.
    :param str service: Used GNSS correction data service.

    """
    # The map uses Spherical Mercator coordinate reference system.
    data = data.to_crs(epsg=3857)
    # Create subplots for horizontal and vertical accuracy.
    fig, (ax1, ax2) = plt.subplots(1, 2)
    # Colors of the plot.
    cmap = "RdYlGn_r"
    scheme = "UserDefined"
    # Classification.
    bins = {"bins": [20, 50, 100, 150, 200, 250, 300, 350, 400, 450, 500]}
    # Plot the horizontal accuracy of the GNSS receiver.
    data.plot(
        column=data["hAcc"],
        ax=ax1,
        legend=True,
        cmap=cmap,
        scheme=scheme,
        classification_kwds=bins
    )
    # Plot the vertical accuracy of the GNSS receiver.
    data.plot(
        column=data["vAcc"],
        ax=ax2,
        legend=True,
        cmap=cmap,
        scheme=scheme,
        classification_kwds=bins
    )
    # Plot config.
    fig.suptitle(f"GNSS Receiver Accuracy\nCorrection service: {service}")
    ax1.set_title("Horizontal accuracy [mm]")
    ax2.set_title("Vertical accuracy [mm]")
    ax1.get_legend().set_bbox_to_anchor((1.0, 1.01))
    ax2.get_legend().set_bbox_to_anchor((1.0, 1.01))
    ax1.axis("off")
    ax2.axis("off")
    # Background map.
    cx.add_basemap(ax1, source=MAPFILE, crs=data.crs)
    cx.add_basemap(ax2, source=MAPFILE, crs=data.crs)
    plt.show()


def main():
    # Download a background map for the plots.
    cx.bounds2raster(
        w=WEST,
        s=SOUTH,
        e=EAST,
        n=NORTH,
        path=MAPFILE,
        source=cx.providers.OpenStreetMap.Mapnik
    )

    filenames = ["position", "position_ntrip", "position_pp"]
    services = ["None", "NTRIP", "PointPerfect"]
    for filename, service in zip(filenames, services):
        data = read_data(filename)
        plot_data(data, service)



if __name__ == "__main__":
    main()
