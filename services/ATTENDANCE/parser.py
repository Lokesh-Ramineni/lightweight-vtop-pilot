from bs4 import BeautifulSoup
import json
import httpx
from pathlib import Path
from email.utils import formatdate
ROOT = Path(__file__).parent.parent.parent
info = ROOT / "config" / "attendance.json"

async def fetching_attendance(html_src,CSRF,client,vtop_engine):
    data=[]
    soup = BeautifulSoup(html_src, "html.parser")
    table=soup.find('table',id="AttendanceDetailDataTable")
    if table is None:
        print("Table not found")
        return
    trs=table.find_all("tr")
    print(len(trs))
    ck = httpx.Cookies()
    ck.set("JSESSIONID", vtop_engine)

    for tr in trs[1:]:
            
            td = tr.find_all("td")
    
            course_text = td[2].find("span").get_text(strip=True)
            course_id, course_name,course_type = map(
                str.strip,
                course_text.split(" - ", 2)
            )

            faculty =td[4].find("span").get_text(strip=True).split('-')[0]

            attended=td[5].find("span").get_text(strip=True)
            total=td[6].find("span").get_text(strip=True)
            percentage=td[7].find("span").get_text(strip=True)
            debar=td[8].find("span").get_text(strip=True)

            onclick = td[9].find("a")["onclick"]

            args = (
                onclick.split("callStudentAttendanceDetailDisplay(")[1]
                .split(")")[0]
                .replace("'", "")
                .split(",")
            )

            semester_id, reg_no, course_id, course_type = args
            postit={
                "_csrf":CSRF,
                "semesterSubId": semester_id,
                "registerNumber":reg_no,
                "courseId":course_id,
                "courseType":course_type,
                "authorizedID": "24MIC7146",
                "x": formatdate(timeval=None, localtime=False, usegmt=True)
            }
            print(
                 postit
            )
            res=await client.post("https://vtop.vitap.ac.in/vtop/processViewAttendanceDetail",data=postit,cookies=ck)
            with open(ROOT / "data" / "cache"/"chech.html","wb") as f:
                f.write(res.content)
            soup1 = BeautifulSoup(res.text, "html.parser")
            table1=soup1.find("table",id="StudentAttendanceDetailDataTable")
            if table1 is None:
                print(f"Attendance table not found for {course_id}")
                with open(ROOT / "data" / "cache" / f"{course_id}_error.html", "w", encoding="utf-8") as f:
                    f.write(res.text)
                continue
            tr_tab=table1.find_all("tr")
            attended_list=[]
            for tr in tr_tab[1:]:
                td=tr.find_all("td")
                attended_list.append({
                    "Sl.No.":td[0].find("span").get_text(strip=True),
                    "Date":td[1].find("span").get_text(strip=True),
                    "Slot":td[2].find("span").get_text(strip=True),
                    "Day / Time":td[3].find("span").get_text(strip=True),
                    "Status":td[4].find("span").get_text(strip=True),
                    "Remarks":td[5].find("span").get_text(strip=True)
                })
            
            data.append({
                "course_id": course_id,
                "course_name": course_name,
                "course_type":course_type,
                "faculty": faculty,
                "attended":attended,
                "total":total,
                "percentage":percentage,
                "debar":debar,
                "attended_list": attended_list
            })
    with open(info,"w") as f:
          json.dump(data,f,indent=4)