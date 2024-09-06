import requests
import pandas as pd
import logging

# Set up logging
logging.basicConfig(
    filename="etl.log",
    filemode="a",
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)


def extract_all_players_from_africa(api_key):
    logging.info("Starting extraction of all players from African countries.")

    BASE_URL = "https://api.brawlstars.com/v1/rankings"
    headers = {"Authorization": f"Bearer {api_key}"}

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

    all_players_data = []

    for country_code in african_country_codes:
        url = f"{BASE_URL}/{country_code}/players"
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            top_players = data.get("items", [])
            for player in top_players:
                player["country_code"] = country_code
            all_players_data.extend(top_players)
            logging.info(f"Successfully fetched data for country code {country_code}.")
        else:
            logging.error(
                f"Failed to fetch data for country code {country_code}: {response.status_code}"
            )

    df_all_players = pd.DataFrame(all_players_data)
    df_all_players.to_csv("all_players_africa.csv", index=False)

    logging.info("Extraction completed, data saved to all_players_africa.csv.")
    return df_all_players
