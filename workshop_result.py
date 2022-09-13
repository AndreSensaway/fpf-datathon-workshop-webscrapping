from bs4 import BeautifulSoup
import requests
import pandas as pd


url_clubs = "https://www.uefa.com/uefachampionsleague/clubs/"
result = requests.get(url_clubs)

doc_clubs = BeautifulSoup(result.text, "html.parser")

group_stage_tag = doc_clubs.find('div', class_="teams-overview_teams-wrapper")
teams_tag = group_stage_tag.find_all('div', class_="team team-is-club")

teams = []
for team_tag in teams_tag:
    team_name = team_tag.a['title']
    team_url = team_tag.a['href']
    team_url = "https://www.uefa.com" + team_url
    
    team = {"name": team_name, "url": team_url}
    
    print(f"Fetching {team_name} data...")
    result = requests.get(team_url)
    doc_team = BeautifulSoup(result.text, "html.parser")

    key_stats_tag = doc_team.find('div', class_="stats-module")
    number_stat_tags = key_stats_tag.find_all('div', class_="stats-module__single-stat--number")

    for stat_tag in number_stat_tags:
        stat_name = stat_tag.find_all('div')[1].string
        stat_value = stat_tag.find_all('div')[0].string

        if "%" in stat_name: stat_value = int(stat_value[:-1])
        if stat_name == "Distance covered (km)": stat_value = float(stat_value)
        else: stat_value = int(stat_value)

        team[stat_name] = stat_value

    teams.append(team)

print(f"___________________________________")   
print(f"Fetched data from {len(teams)} teams")
print("")
print("### All fetched data:")


data = pd.DataFrame(teams)
data.to_csv("team_stats.csv")