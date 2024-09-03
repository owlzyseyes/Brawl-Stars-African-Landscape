# This fetches the top 200 players from each African country

import requests
import pandas as pd

# Your Brawl Stars API key
API_KEY = "YOUR_API_KEY"  # Replace YOUR_API_KEY with your actual API key

# Base URL for the API
BASE_URL = "https://api.brawlstars.com/v1/rankings"

# Set the headers with the API key
headers = {"Authorization": f"Bearer {API_KEY}"}

# List of all African country codes
african_country_codes = [
    "DZ",
    "AO",
    "BJ",
    "BW",
    "BF",
    "BI",
    "CV",
    "CM",
    "CF",
    "TD",
    "KM",
    "CD",
    "CG",
    "CI",
    "DJ",
    "EG",
    "GQ",
    "ER",
    "SZ",
    "ET",
    "GA",
    "GM",
    "GH",
    "GN",
    "GW",
    "KE",
    "LS",
    "LR",
    "LY",
    "MG",
    "MW",
    "ML",
    "MR",
    "MU",
    "MA",
    "MZ",
    "NA",
    "NE",
    "NG",
    "RW",
    "ST",
    "SN",
    "SC",
    "SL",
    "SO",
    "ZA",
    "SS",
    "SD",
    "TZ",
    "TG",
    "TN",
    "UG",
    "ZM",
    "ZW",
]

# Initialize an empty list to store all players data
all_players_data = []

# Loop through each African country code
for country_code in african_country_codes:
    # Construct the request URL
    url = f"{BASE_URL}/{country_code}/players"

    # Make the API request
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

        # Extract the top 500 players
        top_players = data.get("items", [])

        # Add a country code to each player entry
        for player in top_players:
            player["country_code"] = country_code

        # Add to the list of all players
        all_players_data.extend(top_players)
    else:
        print(
            f"Failed to fetch data for country code {country_code}: {response.status_code}"
        )

# Convert the list of players data into a DataFrame
df = pd.DataFrame(all_players_data)

# Display the first few rows of the DataFrame
print(df.head())

# Save the DataFrame to a CSV file (optional)
df.to_csv("top_200_players_africa.csv", index=False)

# Took ~6 minutes to run
# Fetched on 30 August 2023, around 7pm
