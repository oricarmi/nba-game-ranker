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
        teams = game.select(".teams a")
        score_text = game.select_one(".right").text.strip()
        if teams and score_text:
            team1, team2 = teams[0].text, teams[1].text
            scores = [int(s) for s in score_text.split() if s.isdigit()]
            overtime = "OT" in game.text
            games.append({
                "team1": team1, "team2": team2,
                "score1": scores[0], "score2": scores[1],
                "overtime": overtime, "score_diff": abs(scores[0] - scores[1])
            })
    return games

def scrape_news():
    url = "https://www.espn.com/nba/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    articles = soup.select(".contentItem__title")
    yesterday = (datetime.now() - timedelta(1)).strftime("%Y-%m-%d")
    return [article.text for article in articles if yesterday in article.text]