import osmnx as ox
import geopandas as gpd
import pandas as pd
import logging

# Set up logging
logging.basicConfig(
    filename="extract_geometries.log",
    filemode="a",
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)


def extract_and_save_geometries(countries, output_file):
    """
    Extract geometries for a list of countries using osmnx and save as a GeoJSON file.

    Args:
        countries (list): List of country names.
        output_file (str): Path to the output GeoJSON file.

    Returns:
        None
    """
    # Initialize an empty list to store GeoDataFrames
    gdfs = []

    for country in countries:
        try:
            logging.info(f"Extracting geometry for {country}.")
            # Fetch the country geometry using osmnx
            gdf = ox.geocode_to_gdf(country)

            # Check if the GeoDataFrame is not empty
            if not gdf.empty:
                gdfs.append(gdf)
                logging.info(f"Successfully fetched geometry for {country}.")
            else:
                logging.warning(f"No data found for {country}.")

        except Exception as e:
            logging.error(f"Error fetching geometry for {country}: {e}")

    # Combine all the individual GeoDataFrames into one
    if gdfs:
        combined_gdf = pd.concat(gdfs, ignore_index=True)
        # Save the combined GeoDataFrame as a GeoJSON file
        combined_gdf.to_file(output_file, driver="GeoJSON")
        logging.info(f"Geometries saved to {output_file}.")
    else:
        logging.info("No geometries were fetched.")


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

# Run the function
extract_and_save_geometries(countries, "african_countries.geojson")
