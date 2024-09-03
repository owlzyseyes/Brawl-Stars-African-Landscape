# This fetches the player info for the top 200 players fetched by scripts/script_rankings.py

import pandas as pd
import requests
import time

df = pd.read_csv("top_200_africa.csv")

API_KEY = "YOUR_API_KEY"  # Replace YOUR_API_KEY with your actual API key
BASE_URL = "https://api.brawlstars.com/v1/players/"

headers = {"Authorization": f"Bearer {API_KEY}"}

player_tags = df["tag"].tolist()

all_player_data = []

print(len(player_tags))

for player_tag in player_tags:
    # Replace # with %23 for URL encoding
    encoded_tag = player_tag.replace("#", "%23")
    url = f"{BASE_URL}{encoded_tag}"

    # Make the API request
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        # Parse the JSON response
        player_data = response.json()

        # Remove the 'brawlers' key if it exists
        if "brawlers" in player_data:
            del player_data["brawlers"]

        # Add the remaining player data to the list
        all_player_data.append(player_data)
    else:
        print(
            f"Failed to fetch data for player tag {player_tag}: {response.status_code}"
        )

    # To avoid hitting the rate limit, sleep for a short period between requests
    print(player_data)

players_df = pd.DataFrame(all_player_data)

players_df.to_csv("brawl_stars_player_data_no_brawlers.csv", index=False)

print(
    "Player data (excluding brawlers) saved to brawl_stars_player_data_no_brawlers.csv"
)

# Took ~1.5 hours to run
# Fetched on 31 August 2023, around 4pm
