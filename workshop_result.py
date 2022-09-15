from bs4 import BeautifulSoup
import requests
import pandas as pd


url_clubs = "https://www.uefa.com/uefachampionsleague/clubs/"

result = requests.get(url_clubs)  # request page html

doc_clubs = BeautifulSoup(result.text, "html.parser")  # initialize bs4 class instance

group_stage_tag = doc_clubs.find('div', class_="teams-overview_teams-wrapper")  # return div with all relevant clubs
teams_tag = group_stage_tag.find_all('div', class_="team team-is-club")  # return list with each club's div

teams = []
for team_tag in teams_tag:  # loop through teams
    # get club name and url
    team_name = team_tag.a['title']
    team_url = team_tag.a['href']
    team_url = "https://www.uefa.com" + team_url
    
    # creat team data structure
    team = {"name": team_name, "url": team_url}
    
    # request club page html
    print(f"Fetching {team_name} data...")
    result = requests.get(team_url)
    doc_team = BeautifulSoup(result.text, "html.parser")

    key_stats_tag = doc_team.find('div', class_="stats-module")  # return div with all relevant stats
    number_stat_tags = key_stats_tag.find_all('div', class_="stats-module__single-stat--number")  # return list with each stats' div

    for stat_tag in number_stat_tags:  # loop through stats
        # get stat name and value
        stat_name = stat_tag.find(slot="stat-label").string
        stat_value = stat_tag.find(slot="stat-value").string

        # convert values into correct data type
        if "%" in stat_name: stat_value = float(stat_value[:-1])
        elif stat_name == "Distance covered (km)": stat_value = float(stat_value)
        else: stat_value = int(stat_value)
        
        # add stat to team data structure
        team[stat_name] = stat_value

    teams.append(team)

print(f"___________________________________")   
print(f"Fetched data from {len(teams)} teams")
print("")
print("### All fetched data:")

# dave data to csv
data = pd.DataFrame(teams)
data.to_csv("team_stats.csv")