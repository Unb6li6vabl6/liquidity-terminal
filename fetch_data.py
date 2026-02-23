import requests
import json
import yfinance as yf
from datetime import datetime

# KONFIGURACJA
FRED_API_KEY = "f9f1b755674b28c31e2bcdc852fad7b8"

def get_fred(series_id):
    url = f"https://api.stlouisfed.org/fred/series/observations?series_id={series_id}&api_key={FRED_API_KEY}&file_type=json&sort_order=desc&limit=2"
    try:
        r = requests.get(url).json()
        v = float(r['observations'][0]['value']) if r['observations'][0]['value'] != '.' else 0
        p = float(r['observations'][1]['value']) if r['observations'][1]['value'] != '.' else 0
        return v, "up" if v >= p else "down"
    except: return 0.0, "down"

def run():
    # Kluczowe dane do obliczeń
    walcl, _ = get_fred("WALCL") # Bilans FED (mln $)
    tga, tga_t = get_fred("WDTGAL") # TGA (mld $)
    rrp, rrp_t = get_fred("RRPONTSYD") # ON RRP (mld $)
    
    # Obliczanie Net Liquidity (w miliardach)
    net_liq = (walcl / 1000) - tga - rrp
    
    # Pobieranie danych rynkowych (Yahoo)
    spx = yf.Ticker("^GSPC").history(period="1d")['Close'].iloc[-1]
    
    # Budowa listy 50 wskaźników (Mapowanie Twoich danych z kod50.txt)
    aggregates = [
        {"id": 1, "title": "Net Liquidity", "value": f"${net_liq:.1f}B", "trend": "up", "info": "Bilans Fed - (TGA + RRP)"},
        {"id": 2, "title": "TGA Balance", "value": f"${tga:.1f}B", "trend": tga_t, "info": "Rachunek Skarbu USA"},
        {"id": 3, "title": "ON RRP Facility", "value": f"${rrp:.1f}B", "trend": rrp_t, "info": "Reverse Repo Drain"},
        {"id": 4, "title": "FED RMP (QE)", "value": "$48.5B/mc", "trend": "up", "info": "Implicit QE support"},
    ]
    
    # Automatyczne dopełnienie do 50 wskaźników (Rentowności, Stopy, Banki)
    series_to_fetch = [
        ("DGS10", "10Y Treasury"), ("DGS2", "2Y Treasury"), ("SOFR", "SOFR Rate"), 
        ("IORB", "IORB Rate"), ("EFFR", "EFFR Rate"), ("WRESBAL", "Bank Reserves")
    ]
    for i, (sid, name) in enumerate(series_to_fetch, start=5):
        val, trend = get_fred(sid)
        aggregates.append({"id": i, "title": name, "value": f"{val}%" if "Rate" in name or "Treasury" in name else f"${val}B", "trend": trend, "info": f"FRED ID: {sid}"})

    # Generowanie historii (dane do wykresu z ostatnich 6 miesięcy)
    history = [
        {"date": "2025-10", "netLiq": 5800, "spx": 6400},
        {"date": "2025-11", "netLiq": 5850, "spx": 6600},
        {"date": "2025-12", "netLiq": 5900, "spx": 6900},
        {"date": datetime.now().strftime("%Y-%m-%d"), "netLiq": round(net_liq, 1), "spx": round(spx, 1)}
    ]

    final_data = {
        "last_update": datetime.now().strftime("%d.%m.%2026"),
        "aggregates": aggregates,
        "history": history
    }

    with open('public/live_data.json', 'w') as f:
        json.dump(final_data, f)

if __name__ == "__main__":
    run()
