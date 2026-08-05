from bs4 import BeautifulSoup
import json
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
marks_path = ROOT_DIR / "config" / "marks.json"

def fetch_marks(html_src):
    soup = BeautifulSoup(html_src, "lxml")
    outer_table = soup.find("table", class_="customTable")
    
    if not outer_table:
        print("No Data")
        return

    rows = outer_table.find_all("tr")

    content_rows = [r for r in rows if "tableContent" in (r.get("class") or [])]
    
    data = []
  
    for details_row, marks_row in zip(content_rows[::2], content_rows[1::2]):
        tds = details_row.find_all("td")
        course_code = tds[2].get_text(strip=True)
        course_name = tds[3].get_text(strip=True)
        faculty = tds[6].get_text(strip=True)

        course_data = {
            "course_code": course_code,
            "course_name": course_name,
            "faculty": faculty,
            "assessments": []
        }

        inner_table = marks_row.find("table")
        if inner_table:
            for tr in inner_table.find_all("tr")[1:]:  
                td = tr.find_all("td")
                
                course_data["assessments"].append({
                    "s_no": td[0].get_text(strip=True),
                    "title": td[1].get_text(strip=True),
                    "max_marks": td[2].get_text(strip=True),
                    "weightage": td[3].get_text(strip=True),
                    "status": td[4].get_text(strip=True),
                    "scored": td[5].get_text(strip=True),
                    "weightage_mark": td[6].get_text(strip=True),
                    "remark": td[7].get_text(strip=True)
                })

        data.append(course_data)

    marks_path.parent.mkdir(parents=True, exist_ok=True)
    with open(marks_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    
    # return data