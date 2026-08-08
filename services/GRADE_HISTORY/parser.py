from bs4 import BeautifulSoup
from pathlib import Path
import json
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
hist=ROOT_DIR/"config"/"grade_history.json"

def fetch_grade_history(html_src):
    soup = BeautifulSoup(html_src,'lxml')
    tabel1 = soup.find_all('table')[1]
    tabel2=soup.find_all('table')[2]
    if not tabel1:
        print("table1 not found")
        return
    if not tabel2:
        print("table2 not found")
        return
    data=[]
    for row in tabel1.find_all('tr', class_='tableContent', id=False)[2:]:
        s_no=row.find_all('td')[0].get_text(strip=True)
        course=row.find_all('td')[1].get_text(strip=True)
        course_title=row.find_all('td')[2].get_text(strip=True)
        course_type=row.find_all('td')[3].get_text(strip=True)
        credits=row.find_all('td')[4].get_text(strip=True)
        grade=row.find_all('td')[5].get_text(strip=True)

        data.append({
            's_no':s_no,
            'course':course,
            'course_title':course_title,
            'course_type':course_type,
            'credits':credits,
            'grade':grade
        })

    hist.parent.mkdir(parents=True, exist_ok=True)
    with open(hist,"w",encoding="utf-8") as f:
        json.dump(data,f,ensure_ascii=False,indent=4)
