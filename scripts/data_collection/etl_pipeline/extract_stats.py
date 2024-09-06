import pandas as pd
import requests
import logging

# Set up logging
logging.basicConfig(
    filename="etl.log",
    filemode="a",
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)


def extract_player_stats(api_key, csv_file="all_players_africa.csv"):
    logging.info(f"Starting extraction of player stats from {csv_file}.")

    df = pd.read_csv(csv_file)
    player_tags = df["tag"].tolist()

    BASE_URL = "https://api.brawlstars.com/v1/players/"
    headers = {"Authorization": f"Bearer {api_key}"}

    all_player_data = []

    logging.info(f"Total players to process: {len(player_tags)}")

    for player_tag in player_tags:
        encoded_tag = player_tag.replace("#", "%23")
        url = f"{BASE_URL}{encoded_tag}"
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            player_data = response.json()
            if "brawlers" in player_data:
                del player_data["brawlers"]
            all_player_data.append(player_data)
            logging.info(f"Successfully fetched data for player tag {player_tag}.")
        else:
            logging.error(
                f"Failed to fetch data for player tag {player_tag}: {response.status_code}"
            )

    players_df = pd.DataFrame(all_player_data)
    players_df.to_csv("player_stats.csv", index=False)

    logging.info("Player stats extraction completed, data saved to player_stats.csv.")
    return players_df
