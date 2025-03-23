import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
import folium
import plotly.express as px
import seaborn as sns

# Load geographic data
migdf = gpd.read_file('mi.json')
ncgdf = gpd.read_file('nc.json')

# Load data
data = pd.read_csv('data.csv')
ncdata = data[:24]
midata = data[24:]

# Prepare NC data
ncgdf["ZCTA5CE10"] = ncgdf["ZCTA5CE10"].astype(str)
ncdata["ZIP Code"] = ncdata["ZIP Code"].astype(str)

merged_data = ncgdf.merge(ncdata, left_on="ZCTA5CE10", right_on="ZIP Code", how="left")

if "latitude" not in ncdata.columns or "longitude" not in ncdata.columns:
    merged_data["centroid"] = merged_data.geometry.centroid
    merged_data["latitude"] = merged_data["centroid"].y
    merged_data["longitude"] = merged_data["centroid"].x

# Filter out areas without data
ncgdf_with_data = ncgdf[ncgdf["ZCTA5CE10"].isin(ncdata["ZIP Code"])]

m = folium.Map(location=[35.227085, -80.843124], zoom_start=10)
folium.Choropleth(
    geo_data=ncgdf_with_data,
    name="Income Inequality",
    data=ncdata,
    columns=["ZIP Code", "Gini Index"],
    key_on="feature.properties.ZCTA5CE10",
    fill_color="YlOrRd",
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name="Gini Index"
).add_to(m)

for _, row in merged_data.iterrows():
    if pd.notna(row["latitude"]) and pd.notna(row["longitude"]):
        folium.CircleMarker(
            location=[row["latitude"], row["longitude"]],
            radius=row["Vacancy Rates"] * 30,
            color="blue",
            fill=True,
            fill_opacity=0.6,
            popup=f"ZIP Code: {row['ZIP Code']}<br>"
                  f"Housing Price: ${row['Median Home Value']:,}<br>"
                  f"Median Household Income: {row['Median Household Income']:f}"
        ).add_to(m)

# Prepare MI data
migdf["ZCTA5CE10"] = migdf["ZCTA5CE10"].astype(str)
midata["ZIP Code"] = midata["ZIP Code"].astype(str)

merged_data_mi = migdf.merge(midata, left_on="ZCTA5CE10", right_on="ZIP Code", how="left")

if "latitude" not in midata.columns or "longitude" not in midata.columns:
    merged_data_mi["centroid"] = merged_data_mi.geometry.centroid
    merged_data_mi["latitude"] = merged_data_mi["centroid"].y
    merged_data_mi["longitude"] = merged_data_mi["centroid"].x

# Filter out areas without data
migdf_with_data = migdf[migdf["ZCTA5CE10"].isin(midata["ZIP Code"])]

m2 = folium.Map(location=[42.3297, -83.0425], zoom_start=10)
folium.Choropleth(
    geo_data=migdf_with_data,
    name="Income Inequality",
    data=midata,
    columns=["ZIP Code", "Gini Index"],
    key_on="feature.properties.ZCTA5CE10",
    fill_color="YlOrRd",
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name="Gini Index"
).add_to(m2)

for _, row in merged_data_mi.iterrows():
    if pd.notna(row["latitude"]) and pd.notna(row["longitude"]):
        folium.CircleMarker(
            location=[row["latitude"], row["longitude"]],
            radius=row["Vacancy Rates"] * 30,
            color="blue",
            fill=True,
            fill_opacity=0.6,
            popup=f"ZIP Code: {row['ZIP Code']}<br>"
                  f"Housing Price: ${row['Median Home Value']:,}<br>"
                  f"Median Household Income: {row['Median Household Income']:f}"
        ).add_to(m2)

m.save("north_carolina_map_clean.html")
m2.save("michigan_map_clean.html")
