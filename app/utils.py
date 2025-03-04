# app/utils.py
from datetime import datetime, timedelta

def get_yesterday():
    return (datetime.now() - timedelta(1)).strftime("%Y-%m-%d")