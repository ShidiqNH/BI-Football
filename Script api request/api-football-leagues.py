import requests
import csv
import os

# API details
base_url = "https://v3.football.api-sports.io"
headers = {
    "x-rapidapi-host": "v3.football.api-sports.io",
    "x-rapidapi-key": "API-Key"  # Replace with your actual API key
}

# Step 1: Get leagues in Indonesia directly
def get_indonesian_leagues():
    url = f"{base_url}/leagues"
    querystring = {"country": "Indonesia"}
    try:
        response = requests.get(url, headers=headers, params=querystring)
        data = response.json()

        # Print the response to verify the data
        print("Leagues Response:")
        print(data)

        # Check if the response contains data
        if data.get('response'):
            return data['response']
        else:
            return []
    except requests.RequestException as e:
        print(f"Request error: {e}")
        return []

# Step 2: Extract league details and write to CSV
def write_leagues_to_csv(leagues):
    # Ensure the csv folder exists
    csv_folder = 'csv'
    if not os.path.exists(csv_folder):
        os.makedirs(csv_folder)

    csv_file = os.path.join(csv_folder, 'indonesian_leagues.csv')
    csv_columns = ['league_id', 'league_name', 'country', 'season', 'logo']

    try:
        with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=csv_columns, quoting=csv.QUOTE_ALL)
            writer.writeheader()

            for league in leagues:
                league_info = league['league']
                country_info = league['country']
                seasons = league['seasons']
                
                # Handle multiple seasons
                for season in seasons:
                    row = {
                        'league_id': league_info.get('id'),
                        'league_name': league_info.get('name'),
                        'country': country_info.get('name'),
                        'season': season.get('year'),
                        'logo': league_info.get('logo')
                    }

                    # Debugging: print each row before writing
                    print(f"Writing row: {row}")

                    writer.writerow(row)

        print(f"Data has been written to {csv_file} successfully.")
    except Exception as e:
        print(f"Error writing to CSV file: {e}")

# Get Indonesian leagues
indonesian_leagues = get_indonesian_leagues()

# Write leagues to CSV
if indonesian_leagues:
    write_leagues_to_csv(indonesian_leagues)
else:
    print("No leagues found for Indonesia.")
