# app/ranker.py
from transformers import pipeline

sentiment_analyzer = pipeline("sentiment-analysis", model="distilbert-base-uncased")

def rank_excitement(texts):
    excitement_score = 0
    for text in texts:
        result = sentiment_analyzer(text)[0]
        if result["label"] == "POSITIVE" and result["score"] > 0.7:
            if any(word in text.lower() for word in ["thriller", "buzzer-beater", "overtime", "close"]):
                excitement_score += result["score"]
    return excitement_score

def rank_games(games, news_texts):
    ranked_games = []
    for game in games:
        game_text = [t for t in news_texts if game["team1"] in t or game["team2"] in t]
        excitement = rank_excitement(game_text)
        score = (10 if game["overtime"] else 0) + (10 - game["score_diff"]) + excitement
        ranked_games.append(
            {"game": f"{game['team1']} vs {game['team2']}",
             "score_diff": game["score_diff"],
             "score": score})
    return sorted(ranked_games, key=lambda x: x["score"], reverse=True)[:3]