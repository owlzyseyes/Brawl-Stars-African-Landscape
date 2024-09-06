import logging
from extract_players import extract_all_players_from_africa
from extract_stats import extract_player_stats
from extract_geometries import extract_and_save_geometries
from transform import transform_data
from load import load_data

def main():
    logging.basicConfig(level=logging.INFO)
    
    logging.info("Starting the data pipeline.")
    
    # Step 1: Extract players
    players_data = extract_all_players_from_africa()
    logging.info("Players data extracted.")
    
    # Step 2: Extract stats
    stats_data = extract_player_stats()
    logging.info("Stats data extracted.")
    
    # Step 3: Extract geometries
    geometries_data = extract_and_save_geometries()
    logging.info("Geometries data extracted.")
    
    # Step 4: Transform data
    transformed_data = transform_data(players_data, stats_data, geometries_data)
    logging.info("Data transformed.")
    
    # Step 5: Load data
    load_data(transformed_data)
    logging.info("Data loaded into clean_data.geojson.")
    
    logging.info("Data pipeline completed successfully.")

if __name__ == "__main__":
    main()