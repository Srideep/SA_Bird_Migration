# Importing pandas
import pandas as pd
# Importing GeoPandas
import geopandas as gpd

from shapely.geometry import LineString

birds_df = pd.read_csv("../input/geospatial-learn-course-data/purple_martin.csv", parse_dates=['timestamp'])
print("There are {} different birds in the dataset.".format(birds_df["tag-local-identifier"].nunique()))
birds_df.head()
#   Create the GeoDataFrame
birds = gpd.GeoDataFrame(birds_df, geometry=gpd.points_from_xy(birds_df['location-long'], birds_df['location-lat']))

#   Set the CRS to {'init': 'epsg:4326'}
birds.crs = {'init': 'epsg:4326'}

# Load a GeoDataFrame with country boundaries in North/South America, print the first 5 rows
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
americas = world.loc[world['continent'].isin(['North America', 'South America'])]
americas.head()
# Load the data and print the first 5 rows of the birds migration dataset
birds_df = pd.read_csv("../input/geospatial-learn-course-data/purple_martin.csv", parse_dates=['timestamp'])
print("There are {} different birds in the dataset.".format(birds_df["tag-local-identifier"].nunique()))
birds_df.head()

# GeoDataFrame showing path for each bird

path_df = birds.groupby("tag-local-identifier")['geometry'].apply(list).apply(lambda x: LineString(x)).reset_index()
path_gdf = gpd.GeoDataFrame(path_df, geometry=path_df.geometry)
path_gdf.crs = {'init' :'epsg:4326'}

# GeoDataFrame showing starting point for each bird
start_df = birds.groupby("tag-local-identifier")['geometry'].apply(list).apply(lambda x: x[0]).reset_index()
start_gdf = gpd.GeoDataFrame(start_df, geometry=start_df.geometry)
start_gdf.crs = {'init' :'epsg:4326'}

# Show first five rows of GeoDataFrame
start_gdf.head()

end_df = birds.groupby("tag-local-identifier")['geometry'].apply(list).apply(lambda x: x[-1]).reset_index()
end_gdf = gpd.GeoDataFrame(end_df, geometry=end_df.geometry)
end_gdf.crs = {'init' :'epsg:4326'}
end_gdf.head()

ax = americas.plot(figsize=(8,8), color='white', linestyle=':', edgecolor='gray')
path_gdf.plot(markersize=10, ax=ax)
start_gdf.plot(markersize=10,ax=ax)
end_gdf.plot(markersize=10,ax=ax)

# Path of the shapefile to load
protected_filepath = "../input/geospatial-learn-course-data/SAPA_Aug2019-shapefile/SAPA_Aug2019-shapefile/SAPA_Aug2019-shapefile-polygons.shp"

# Protected Area File Read
protected_areas = gpd.read_file(protected_filepath)

# Country boundaries in South America
south_america = americas.loc[americas['continent']=='South America']

# Plot of the  protected areas in South America
ax = south_america.plot(figsize=(8,8), color='white', linestyle=':', edgecolor='gray')

P_Area = sum(protected_areas['REP_AREA']-protected_areas['REP_M_AREA'])
print("South America has {} square kilometers of protected areas.".format(P_Area))
south_america.head()

#  Calculation of the total area of South America (in square kilometers)
totalArea = sum(south_america.to_crs(epsg=3035).geometry.area / 10**6)
print(totalArea)

# Calculation of  percentage of South America protected areas ?
percentage_protected = P_Area/totalArea
print('Approximately {}% of South America is protected.'.format(round(percentage_protected*100, 2)))

# Plot of the Protected Areas in South America
ax = south_america.plot(figsize=(8,8), color='white', linestyle=':', edgecolor='gray')
protected_areas[protected_areas['MARINE']!='2'].plot(markersize=5, ax=ax)