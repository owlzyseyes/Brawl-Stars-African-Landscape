# This script fetches data from OpenStreetMap

import osmnx as ox
import geopandas as gpd
import pandas as pd

# List of African countries
countries = [
    "Algeria",
    "Angola",
    "Benin",
    "Botswana",
    "Burkina Faso",
    "Burundi",
    "Cape Verde",
    "Cameroon",
    "Central African Republic",
    "Chad",
    "Comoros",
    "Democratic Republic of the Congo",
    "Republic of the Congo",
    "Ivory Coast",
    "Djibouti",
    "Egypt",
    "Equatorial Guinea",
    "Eritrea",
    "Eswatini",
    "Ethiopia",
    "Gabon",
    "Gambia",
    "Ghana",
    "Guinea",
    "Guinea-Bissau",
    "Kenya",
    "Lesotho",
    "Liberia",
    "Libya",
    "Madagascar",
    "Malawi",
    "Mali",
    "Mauritania",
    "Mauritius",
    "Morocco",
    "Mozambique",
    "Namibia",
    "Niger",
    "Nigeria",
    "Rwanda",
    "Sao Tome and Principe",
    "Senegal",
    "Seychelles",
    "Sierra Leone",
    "Somalia",
    "South Africa",
    "South Sudan",
    "Sudan",
    "Tanzania",
    "Togo",
    "Tunisia",
    "Uganda",
    "Zambia",
    "Zimbabwe",
]

# Download and process polygons for each country
gdfs = []
for country in countries:
    gdf = ox.geocode_to_gdf(country)
    gdfs.append(gdf)

# Combine into a single GeoDataFrame
combined_gdf = pd.concat(gdfs, ignore_index=True)

# Save the combined GeoDataFrame as a GeoJSON file
combined_gdf.to_file("african_countries.geojson", driver="GeoJSON")
