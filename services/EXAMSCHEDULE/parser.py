from bs4 import BeautifulSoup
from pathlib import Path
import json
ROOT_DIR=Path(__file__).parent.parent.parent
ex=ROOT_DIR/"config"/"exam.json"
def parse_schedule(html_src):
    soup=BeautifulSoup(html_src,"lxml")
    table = soup.find("table", class_="customTable")
    if table is None:
        print("No data yet")
        return
    schedule={
        "exam_schedule":{}
    }
    current_exam=None
    for row in table.find_all("tr"):
        panel_head=row.find('td',class_="panelHead-secondary")
        if panel_head:
            current_exam=panel_head.get_text(strip=True)
            schedule["exam_schedule"][current_exam]=[]
            continue
        tds=row.find_all('td')
        
        if len(tds) == 13 and current_exam:
            first_cell = tds[0].get_text(strip=True)
            if not first_cell.isdigit():
                continue

            exam_entry = {
                "s_no": int(tds[0].get_text(strip=True)),
                "course_code": tds[1].get_text(strip=True),
                "course_title": tds[2].get_text(strip=True),
                "course_type": tds[3].get_text(strip=True),
                "class_id": tds[4].get_text(strip=True),
                "slot": tds[5].get_text(strip=True),
                "exam_date": tds[6].get_text(strip=True),
                "exam_session": tds[7].get_text(strip=True),
                "reporting_time": tds[8].get_text(strip=True),
                "exam_time": tds[9].get_text(strip=True),
                "venue": tds[10].get_text(strip=True),
                "seat_location": tds[11].get_text(strip=True),
                "seat_no": tds[12].get_text(strip=True)
            }
            schedule["exam_schedule"][current_exam].append(exam_entry)

    ex.parent.mkdir(parents=True, exist_ok=True)
    with open(ex,"w",encoding="utf-8") as f:
        json.dump(schedule,f,indent=4)