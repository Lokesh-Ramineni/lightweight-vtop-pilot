import json
import logging
from pathlib import Path
from bs4 import BeautifulSoup

ROOT_DIR=Path(__file__).resolve().parent.parent.parent
bio=ROOT_DIR/"config"/"biometric.json"

logger = logging.getLogger(__name__)

def fetch_bio(html_src):
    soup=BeautifulSoup(html_src,"lxml")
    table=soup.find("table")
    data=[]
    bio.parent.mkdir(parents=True, exist_ok=True)

    if not table:
        logger.error("No data found")
        with open(bio, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        return
    
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

    with open(bio, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)