import requests
import csv
import os
import time

# API details
url = "https://v3.football.api-sports.io/teams"
headers = {
    "x-rapidapi-host": "v3.football.api-sports.io",
    "x-rapidapi-key": "bc6b867471810c9cb075388982a4a29f"  # Replace with your actual API key
}

# Step 1: Read league IDs from the provided CSV file
def get_leagues_from_csv(csv_file):
    leagues = []
    try:
        with open(csv_file, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header row
            for row in reader:
                if row:
                    leagues.append({
                        'league_id': row[0],
                        'league_name': row[1],
                        'country': row[2],
                        'season': row[3],
                        'logo': row[4]
                    })
    except Exception as e:
        print(f"Error reading leagues CSV file: {e}")
    return leagues

# Step 2: Get teams for a specific league
def get_teams_for_league(league_id, season):
    querystring = {"league": league_id, "season": season}
    try:
        response = requests.get(url, headers=headers, params=querystring)
        response.raise_for_status()  # Raise an error for bad HTTP status codes
        data = response.json()
        if data.get('response'):
            return data['response']
        else:
            print(f"No 'response' field found in API data for league {league_id}.")
            return []
    except requests.RequestException as e:
        print(f"Request error for league {league_id}: {e}")
        return []

# Step 3: Write team details to CSV
def write_teams_to_csv(teams, league_name, season):
    # Ensure the csv folder exists
    csv_folder = 'csv'
    if not os.path.exists(csv_folder):
        os.makedirs(csv_folder)

    # Create a file name based on the league name and season
    csv_file = os.path.join(csv_folder, f'{league_name.lower().replace(" ", "_")}_{season}_teams.csv')
    csv_columns = ['team_id', 'team_name', 'country', 'founded', 'national', 'logo', 
                   'venue_id', 'venue_name', 'address', 'city', 'capacity', 'surface', 'image']

    try:
        with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=csv_columns, quoting=csv.QUOTE_ALL)
            writer.writeheader()
            for team in teams:
                team_info = team.get('team', {})
                venue_info = team.get('venue', {})
                row = {
                    'team_id': team_info.get('id'),
                    'team_name': team_info.get('name'),
                    'country': team_info.get('country'),
                    'founded': team_info.get('founded'),
                    'national': team_info.get('national'),
                    'logo': team_info.get('logo'),
                    'venue_id': venue_info.get('id'),
                    'venue_name': venue_info.get('name'),
                    'address': venue_info.get('address'),
                    'city': venue_info.get('city'),
                    'capacity': venue_info.get('capacity'),
                    'surface': venue_info.get('surface'),
                    'image': venue_info.get('image')
                }
                writer.writerow(row)
        print(f"Data has been written to {csv_file} successfully.")
    except Exception as e:
        print(f"Error writing to CSV file: {e}")

# Main function
def main():
    # Input CSV file with league information
    input_csv_file = 'csv\premier_leagues.csv'

    # Get leagues from the CSV file
    leagues = get_leagues_from_csv(input_csv_file)

    # Fetch teams for each league and write to separate CSV files
    for index, league in enumerate(leagues):
        league_id = league['league_id']
        season = league['season']
        league_name = league['league_name']
        teams = get_teams_for_league(league_id, season)
        if teams:
            write_teams_to_csv(teams, league_name, season)
        else:
            print(f"No teams found for league {league_name}.")
        
        # Sleep to respect API rate limit
        if index < len(leagues) - 1:  # Avoid delay after the last request
            time.sleep(10)

if __name__ == "__main__":
    main()
