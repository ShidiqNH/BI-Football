import requests
import csv
import os

# API details
base_url = "https://v3.football.api-sports.io"
headers = {
    "x-rapidapi-host": "v3.football.api-sports.io",
    "x-rapidapi-key": "API-Key"  # Replace with your actual API key
}

# Function to get teams in a specific league and season
def get_teams_in_league(league_id, season):
    url = f"{base_url}/teams"
    querystring = {"league": league_id, "season": season}
    try:
        response = requests.get(url, headers=headers, params=querystring)
        data = response.json()

        # Print the entire response for debugging
        print(f"Teams API Response for League {league_id} Season {season}:")
        print(data)

        # Check if the response contains data
        if data.get('response'):
            return data['response']
        else:
            return []
    except requests.RequestException as e:
        print(f"Request error: {e}")
        return []

# Function to read leagues from CSV
def read_leagues_from_csv(csv_file):
    leagues = []
    try:
        with open(csv_file, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                leagues.append(row)
        return leagues
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return []

# Function to write teams to CSV
def write_teams_to_csv(teams, league_name, season):
    # Ensure the csv folder exists
    csv_folder = 'csv'
    if not os.path.exists(csv_folder):
        os.makedirs(csv_folder)

    csv_file = os.path.join(csv_folder, f'{league_name}_{season}_football_clubs.csv')
    csv_columns = ['team_id', 'team_name', 'country', 'founded', 'national', 'logo', 
                   'venue_id', 'venue_name', 'address', 'city', 'capacity', 'surface', 'image']

    try:
        with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=csv_columns, quoting=csv.QUOTE_ALL)
            writer.writeheader()

            for team in teams:
                team_info = team['team']
                venue_info = team['venue']
                
                row = {
                    'team_id': team_info.get('id'),
                    'team_name': team_info.get('name'),
                    'country': team_info.get('country'),
                    'founded': team_info.get('founded'),
                    'national': team_info.get('national'),
                    'logo': team_info.get('logo'),
                    'venue_id': venue_info.get('id') if venue_info else None,
                    'venue_name': venue_info.get('name') if venue_info else None,
                    'address': venue_info.get('address') if venue_info else None,
                    'city': venue_info.get('city') if venue_info else None,
                    'capacity': venue_info.get('capacity') if venue_info else None,
                    'surface': venue_info.get('surface') if venue_info else None,
                    'image': venue_info.get('image') if venue_info else None
                }

                # Debugging: print each row before writing
                print(f"Writing row: {row}")

                writer.writerow(row)

        print(f"Data has been written to {csv_file} successfully.")
    except Exception as e:
        print(f"Error writing to CSV file: {e}")

# Read leagues from CSV
leagues = read_leagues_from_csv('indonesian_leagues.csv')

# Process each league and season
for league in leagues:
    league_id = league['league_id']
    league_name = league['league_name'].replace(" ", "-")
    season = league['season']
    csv_file = os.path.join('csv', f'{league_name}_{season}_football_clubs.csv')

    # Check if the CSV file already exists
    if not os.path.exists(csv_file):
        teams = get_teams_in_league(league_id, season)
        if teams:
            write_teams_to_csv(teams, league_name, season)
        else:
            print(f"No teams found for league {league_name} in season {season}.")
    else:
        print(f"CSV file for league {league_name} in season {season} already exists, skipping extraction.")
