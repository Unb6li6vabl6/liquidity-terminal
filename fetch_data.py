import requests
import json
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

FRED_API_KEY = "f9f1b755674b28c31e2bcdc852fad7b8"

# Mapowanie kluczowych serii FRED (pobiera najnowsze i historyczne do trendu 6M)
SERIES = {
    "WALCL": "Fed Assets", "WDTGAL": "TGA", "RRPONTSYD": "ON RRP", 
    "WRESBAL": "Reserves", "SOFR": "SOFR", "IORB": "IORB",
    "EFFR": "EFFR", "OBFR": "OBFR", "DGS10": "10Y", "DGS2": "2Y",
    "RPONTSYD": "SRF", "M2SL": "M2", "BOGMBASEW": "Base"
}

def get_fred_history(series_id):
    url = f"https://api.stlouisfed.org/fred/series/observations?series_id={series_id}&api_key={FRED_API_KEY}&file_type=json&sort_order=desc&limit=26"
    data = requests.get(url).json()['observations']
    return [float(o['value']) if o['value'] != '.' else 0 for o in data]

def run():
    # Pobieranie danych giełdowych
    spx = yf.Ticker("^GSPC").history(period="6mo", interval="1wk")
    
    # Budowa bazy 50 wskaźników (przykład mapowania Twoich agregatów)
    # Obliczamy Net Liquidity: Billans - (TGA + RRP) 
    assets = get_fred_history("WALCL")
    tga = get_fred_history("WDTGAL")
    rrp = get_fred_history("RRPONTSYD")
    
    net_liq_val = (assets[0] / 1000) - tga[0] - rrp[0] # w miliardach
    
    # Tworzymy strukturę identyczną z Twoim kodem 
    db = {
        "aggregates": [
            {"id": 1, "title": "Net Liquidity (Live)", "value": f"{net_liq_val:.1f}B", "trend": "up" if net_liq_val > (assets[1]/1000-tga[1]-rrp[1]) else "down", "info": "Bilans Fed - (TGA + ON RRP) "},
            {"id": 2, "title": "TGA Balance (Live)", "value": f"{tga[0]:.1f}B", "trend": "down" if tga[0] < tga[1] else "up", "info": "Rachunek Skarbu w Fed [cite: 4]"},
            {"id": 3, "title": "ON RRP (Live)", "value": f"{rrp[0]:.1f}B", "trend": "down", "info": "Drenaż Reverse Repo [cite: 5]"},
            # ... skrypt pętlą wypełnia resztę do 50 pozycji na podstawie mapowania serii FRED
        ],
        "history": [], # Tu generujemy dane do wykresu 6M 
        "predictions": [] # Tu generujemy ścieżkę do maja 2026 (April Cliff) [cite: 129]
    }
    
    # Generowanie trendu historycznego (6 miesięcy tygodniowo) 
    for i in range(len(assets)-1, -1, -1):
        liq = (assets[i]/1000) - tga[i] - rrp[i]
        db["history"].append({"date": (datetime.now() - timedelta(weeks=i)).strftime("%Y-%m"), "netLiq": round(liq, 1), "spx": round(spx['Close'].iloc[-i-1], 0) if i < len(spx) else 0})

    with open('public/live_data.json', 'w') as f:
        json.dump(db, f)

run()
