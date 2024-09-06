import pandas as pd
import geopandas as gpd
import logging

def transform_data(player_data_csv, player_stats_csv, geojson_file):
    logging.info("Starting data transformation process.")
    
    try:
        # Define region mapping
        region_mapping = {
    'North Africa': ['Algeria', 'Egypt', 'Libya', 'Morocco', 'Sudan', 'Tunisia',"South Sudan"],
    'East Africa': ['Burundi', 'Comoros', 'Djibouti', 'Eritrea', 'Ethiopia', 'Kenya', 'Rwanda', 'Seychelles', 'Somalia', 'Tanzania', 'Uganda'],
    'West Africa': ['Benin', 'Burkina Faso', 'Cape Verde', 'The Gambia', 'Ghana', 'Guinea', 'Guinea-Bissau', "Côte d'Ivoire", 'Liberia', 'Mali', 'Mauritania', 'Niger', 'Nigeria', 'Senegal', 'Sierra Leone', 'Togo'],
    'Central Africa': ['Cameroon', 'Central African Republic', 'Chad', 'Congo', 'Democratic Republic of the Congo', 'Equatorial Guinea', 'Gabon', 'São Tomé and Príncipe',"Congo-Brazzaville"],
    'Southern Africa': ['Angola', 'Botswana', 'Eswatini', 'Lesotho', 'Madagascar', 'Malawi', 'Mauritius', 'Mozambique', 'Namibia', 'South Africa', 'Zambia', 'Zimbabwe']}
        
        # Reverse the mapping for quick lookup
        country_to_region = {country: region for region, countries in region_mapping.items() for country in countries}

        # Load the player data and stats
        player_data = pd.read_csv(player_data_csv)
        player_stats = pd.read_csv(player_stats_csv)

        #fill country_code missing values in player_data with NA
        player_data["country_code"] = player_data["country_code"].fillna("NA")

        
        # Merge the player data with player stats on the 'tag' column
        merged_data = pd.merge(player_data, player_stats, on='tag')

        #rename trophies_x to trophies
        merged_data.rename(columns={'trophies_x': 'trophies'}, inplace=True)

        #select relevant columns
        merged_data = merged_data[[ 'country_code',"trophies",'3vs3Victories', 'soloVictories', 'duoVictories', 'expLevel', 'expPoints']]
        
        # Group by 'country_code' and aggregate
        aggregated_data = merged_data.groupby('country_code').agg({
            'trophies': 'mean',
            '3vs3Victories': 'mean',
            'soloVictories': 'mean',
            'duoVictories': 'mean',
            'expLevel': 'mean',
            'expPoints': 'mean'
        }).reset_index()

        #round the values to the nearest whole number
        aggregated_data = aggregated_data.round({'trophies': 0, '3vs3Victories': 0, 'soloVictories': 0, 'duoVictories': 0, 'expLevel': 0, 'expPoints': 0})

        # Load the geometries GeoDataFrame
        geometries_gdf = gpd.read_file(geojson_file)

        # Concat the aggregated data with the geometries
        aggregated_gdf = pd.concat([geometries_gdf, aggregated_data], axis=1)

        # Add region information
        aggregated_gdf['region'] = aggregated_gdf['name'].map(country_to_region)

        # Keep only the required columns and drop 'country_code'
        final_gdf = aggregated_gdf[['name', 'geometry', 'importance', 'region', '3vs3Victories', 'soloVictories', 'duoVictories', 'expLevel', 'expPoints']]
        
        # Save the final GeoDataFrame to a GeoJSON file
        final_gdf.to_file("transformed_data.geojson", driver="GeoJSON")

        # Log the completion
        logging.info(f"Data transformation completed successfully.")
        
        return final_gdf
    
    except FileNotFoundError as e:
        logging.error(f"File not found: {e}")
        raise
    except pd.errors.EmptyDataError as e:
        logging.error(f"Empty data error: {e}")
        raise
    except KeyError as e:
        logging.error(f"Missing column: {e}")
        raise
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise
