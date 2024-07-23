import requests
import csv
import os

# API details
url = "https://v3.football.api-sports.io/teams"
querystring = {"country": "Indonesia"}
headers = {
    "x-rapidapi-host": "v3.football.api-sports.io",
    "x-rapidapi-key": "API-Key"  # Replace with your actual API key
}

# Step 1: Get teams in Indonesia directly
def get_indonesian_teams():
    try:
        response = requests.get(url, headers=headers, params=querystring)
        response.raise_for_status()  # Raise an error for bad HTTP status codes
        data = response.json()

        # Print the entire response for debugging
        print("API Response:")
        print(data)

        # Check if the response contains data
        if data.get('response'):
            return data['response']
        else:
            print("No 'response' field found in API data.")
            return []
    except requests.RequestException as e:
        print(f"Request error: {e}")
        return []

# Step 2: Extract team details and write to CSV
def write_teams_to_csv(teams):
    # Ensure the csv folder exists
    csv_folder = 'csv'
    if not os.path.exists(csv_folder):
        os.makedirs(csv_folder)

    csv_file = os.path.join(csv_folder, 'indonesian_football_clubs.csv')
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

                # Debugging: print each row before writing
                print(f"Writing row: {row}")

                writer.writerow(row)

        print(f"Data has been written to {csv_file} successfully.")
    except Exception as e:
        print(f"Error writing to CSV file: {e}")

# Get Indonesian teams
indonesian_teams = get_indonesian_teams()

# Write teams to CSV
if indonesian_teams:
    write_teams_to_csv(indonesian_teams)
else:
    print("No data found for the specified country.")
