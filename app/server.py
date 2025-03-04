# app/server.py
from flask import Flask, render_template
from .scraper import scrape_game_stats, scrape_news
from .ranker import rank_games
import pandas as pd
from datetime import datetime, timedelta

app = Flask(__name__)

@app.route('/')
def home():
    games = scrape_game_stats()
    news = scrape_news()
    top_games = rank_games(games, news)
    yesterday = (datetime.now() - timedelta(1)).strftime("%Y-%m-%d")
    df = pd.DataFrame(top_games)
    df.to_csv(f"data/ranks_{yesterday}.csv", index=False)
    return render_template("index.html", games=top_games, date=yesterday)

@app.route('/history/<date>')
def history(date):
    df = pd.read_csv(f"data/ranks_{date}.csv")
    return render_template("index.html", games=df.to_dict("records"), date=date)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)