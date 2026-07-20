from pathlib import Path
import json
ROOT_DIR = Path(__file__).parent.parent
session=ROOT_DIR / "config" / "session.json"

def save(cookie):
    data={
        "JSESSIONID":cookie["JSESSIONID"],
    }
    with open(session,"w") as f:
        json.dump(data,f)