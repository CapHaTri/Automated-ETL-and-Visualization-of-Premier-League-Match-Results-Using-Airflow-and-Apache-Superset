import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

standings_url = "https://fbref.com/en/comps/9/Premier-League-Stats"
data = requests.get(standings_url)
soup = BeautifulSoup(data.text)
standings_table = soup.select('table.stats_table')[0]

links = standings_table.find_all('a')
links = [l.get("href") for l in links]
links = [l for l in links if '/squads/' in l]

team_urls = [f"https://fbref.com{l}" for l in links]
all_matches = []

for team_url in team_urls:
    team_data = []
    data = ''
    team_name = team_url.split("/")[-1].replace("-Stats", "").replace("-", " ")
    data = requests.get(team_url)
    team_data = pd.read_html(data.text, match="Scores & Fixtures")[0]
    team_data = team_data[team_data["Comp"] == "Premier League"]

    team_data["Team"] = team_name
    all_matches.append(team_data)
    time.sleep(5)

match_df = pd.concat(all_matches)
match_df.columns = [c.lower() for c in match_df.columns]
match_df.to_csv("matches.csv")