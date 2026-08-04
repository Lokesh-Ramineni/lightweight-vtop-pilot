from bs4 import BeautifulSoup
from pathlib import Path
import json

ROOT_DIR=Path(__file__).resolve().parent.parent.parent
bio=ROOT_DIR/"config"/"biometric.json"
def fetch_bio(html_src):
    soup=BeautifulSoup(html_src,"lxml")
    table=soup.find("table")
    if not table:
        print("No data found")
    data=[]
    total_entries=table.find_all('tr')[-1].find_all("td")[0].get_text(strip=True)
    data.append({
        "total_entries":total_entries
    })
    for row in table.find_all('tr')[1:]:
        td=row.find_all("td")
        punch_time=td[2].get_text(strip=True)
        venu=td[3].get_text(strip=True)
        data.append({
            "punch_time":punch_time,
            "venu":venu
        })

    bio.parent.mkdir(parents=True, exist_ok=True)
    
    with open(bio, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)