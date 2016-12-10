import csv
import datetime
import requests
from bs4 import BeautifulSoup

# Preparing the url
BASEURL = 'http://www.espn.com/nba/schedule/_/date/'
now = datetime.datetime.now()
today_date = now.strftime('%Y%m%d')
target_url = BASEURL + today_date


link = requests.get(target_url)
soup = BeautifulSoup(link.text, 'lxml')
tables = soup.findChildren('table')   # Get all table tags
my_table = tables[0]  # The required table is the first, has today's schedule
trs = tables[0].find_all('tr')  # Get all tr tags

first_set_teams, second_set_teams, games_time = ([] for i in range(3))

def extract_team_name(team_info):
    """Extract team name and add it to its corresponding list."""
    team = team_info.findChildren()
    team_name = team[0].string
    if team_info.parent.get('class') == ['home']:
        second_set_teams.append(team_name)
    else:
        first_set_teams.append(team_name)


for tr in trs:
    teams = tr.find_all('a', {'class': 'team-name'})
    games_start_times = tr.find_all('td', {'data-behavior': 'date_time'})

    for team in teams:
        extract_team_name(team)

    for stime in games_start_times:
        value = stime['data-date']
        game_time = value[value.find('T')+1:value.find('Z')]
        games_time.append(game_time)

# write to csv file
with open('schedule.csv', 'w') as csvfile:
    fieldnames = ['team_one_name', 'team_two_name', 'start_time']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    all_in_one = zip(first_set_teams, second_set_teams, games_time) # zip all in a list

    for team_one, team_two, start_time in all_in_one:
        writer.writerow({'team_one_name': team_one, 'team_two_name': team_two, 'start_time': start_time})

csvfile.close()

