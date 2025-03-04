# app/scraper.py
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

def scrape_game_stats():
    yesterday = (datetime.now() - timedelta(1)).strftime("%Y-%m-%d")
    url = f"https://www.basketball-reference.com/boxscores/?month={yesterday[5:7]}&day={yesterday[8:10]}&year={yesterday[0:4]}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    games = []
    for game in soup.select(".game_summary"):
        teams = [t.text.strip() for t in game.select("td:not(.right)")]
        team1 = teams[0]
        team2 = teams[1]
        all_right_elements = game.select("td.right")
        right_only = [elem for elem in all_right_elements if elem.get("class") == ["right"]]
        team1_score = int(right_only[0].text.strip())
        team2_score = int(right_only[1].text.strip())
        if team1 and team2 and team1_score and team2_score:
            overtime = "OT" in game.text
            games.append({
                "team1": team1, "team2": team2,
                "score1": team1_score, "score2": team2_score,
                "overtime": overtime, "score_diff": abs(team1_score - team2_score)
            })
    return games

def scrape_news():
    url = "https://www.espn.com/nba/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    articles = soup.select(".contentItem__title")
    yesterday = (datetime.now() - timedelta(1)).strftime("%Y-%m-%d")
    return [article.text for article in articles if yesterday in article.text]