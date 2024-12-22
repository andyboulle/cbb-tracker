import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime, timedelta
from config import config

# This function gets all the game objects from the given month-day-year from the API
def get_yesterdays_games(year, month, day, api_key):
    url = f'https://api.sportsdata.io/v3/cbb/scores/json/GamesByDateFinal/{year}-{month}-{day}?key={api_key}'
    response = requests.get(url)

    games = []
    for game in response.json():
        games.append(game)

    return games

# This function filters the games to only return games that include the given teams
def filter_games_by_teams(games, teams):
    filtered_games = []
    for game in games:
        if game['HomeTeam'] in teams or game['AwayTeam'] in teams:
            if game['HomeTeamScore'] != None and game['AwayTeamScore'] != None:
                filtered_games.append(game)
        
    return filtered_games

# This function gets the results of the games for the passed teams
def get_game_results(games, teams):
    results = []
    for game in games:
        if game['HomeTeam'] in teams:
            results.append(
                {
                    'team': game['HomeTeam'],
                    'points': game['HomeTeamScore'],
                    'opponent': game['AwayTeam'],
                    'opponent_points': game['AwayTeamScore'],
                    'result': 'W' if game['HomeTeamScore'] > game['AwayTeamScore'] else 'L'
                }
            )
        else:
            results.append(
                {
                    'team': game['AwayTeam'],
                    'points': game['AwayTeamScore'],
                    'opponent': game['HomeTeam'],
                    'opponent_points': game['HomeTeamScore'],
                    'result': 'W' if game['AwayTeamScore'] > game['HomeTeamScore'] else 'L'
                }
            )

    return results

# This function determines the daily record of the teams based on the results
def determine_daily_record(results):
    wins = 0
    losses = 0
    
    for result in results:
        if result['result'] == 'W':
            wins += 1
        else:
            losses += 1

    return f'{wins}-{losses}'

# This function gets the information of the teams from the API
def get_teams_info(api_key, team_keys):
    url = f'https://api.sportsdata.io/v3/cbb/scores/json/teams?key={api_key}'
    response = requests.get(url)

    teams = []

    for team in response.json():
        if team['Key'] in team_keys:
            teams.append(team)

    return teams

# This function gets the records of the teams passed
def get_teams_records(teams):
    team_records = []

    for team in teams:
        team_records.append(
            {
                'team': team['School'],
                'record': f'{team['Wins']}-{team['Losses']}'
            }
        )

    return team_records

# This function gets the season record of the all the teams combined
def get_season_record(team_records):
    wins = 0
    losses = 0

    for record in team_records:
        record_parts = record['record'].split('-')
        wins += int(record_parts[0])
        losses += int(record_parts[1])

    return f'{wins}-{losses}'

# This function generates the daily report. It includes the following:
# - Yesterday's Record
# - Season Record
# - Yesterday's Results
# - Updated Team Records
def generate_daily_report(results, team_records, daily_record, season_record):
    report = f'DAILY CBB REPORT: {(datetime.now() - timedelta(1)).strftime('%m/%d/%Y')}\n'
    report += '---------------------------------------------\n'
    report += f'Yesterday\'s Record: {daily_record}\n'
    report += f'Season Record: {season_record}\n\n'
    report += f'Yesterday\'s Results:\n'
    for result in results:
        report += f'{result["team"]} {result["points"]} - {result["opponent_points"]} {result["opponent"]} ({result['result']})\n'

    sorted_teams = sorted(team_records, key=lambda x: x['record'].split('-')[0], reverse=True)
    report += f'\nUpdated Team Records:\n'
    for record in sorted_teams:
        report += f'{record["team"]}: {record["record"]}\n'

    return report

# This function sends the report as an email
def send_report_email(report):
    msg = MIMEMultipart()
    msg['From'] = config['FROM_EMAIL']
    msg['To'] = config['TO_EMAIL']
    msg['Subject'] = 'Daily CBB Report'
    msg.attach(MIMEText(report, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(config['FROM_EMAIL'], config['FROM_PASSWORD'])
    server.send_message(msg)
    server.quit()

def main():
    api_key = config['API_KEY']
    team_abbreviations = config['TEAMS']

    # Get yesterday's date into the right variables
    yesterdays_date = datetime.now() - timedelta(1)
    yesterdays_date_str = yesterdays_date.strftime('%Y-%b-%d')
    yesterdays_date_parts = yesterdays_date_str.split('-')
    year = yesterdays_date_parts[0]
    month = yesterdays_date_parts[1]
    day = yesterdays_date_parts[2]

    # Get yesterday's games, results, and records
    yesterdays_games = get_yesterdays_games(year, month, day, api_key)
    filtered_games = filter_games_by_teams(yesterdays_games, team_abbreviations)
    game_results = get_game_results(filtered_games, team_abbreviations)
    daily_record = determine_daily_record(game_results)

    # Get team records and calculate season record
    teams = get_teams_info(api_key, team_abbreviations)
    team_records = get_teams_records(teams)
    season_record = get_season_record(team_records)

    # Generate and send the daily report
    report = generate_daily_report(game_results, team_records, daily_record, season_record)
    send_report_email(report)
    print(report)

main()

