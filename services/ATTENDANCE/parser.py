import asyncio
import json
from email.utils import formatdate
from pathlib import Path

import httpx
from bs4 import BeautifulSoup

ROOT = Path(__file__).parent.parent.parent
INFO = ROOT / "config" / "attendance.json"

URL = "https://vtop.vitap.ac.in/vtop/processViewAttendanceDetail"


async def fetch_course(client, cookies, csrf, course):
    post_data = {
        "_csrf": csrf,
        "semesterSubId": course["semester_id"],
        "registerNumber": course["reg_no"],
        "courseId": course["course_id_arg"],
        "courseType": course["course_type_arg"],
        "authorizedID": "24MIC7146",  
        "x": formatdate(usegmt=True),
    }

    try:
        res = await client.post(URL, data=post_data, cookies=cookies)
        res.raise_for_status()
    except Exception as e:
        print(f"Failed to fetch {course['course_id']}: {e}")
        course["attended_list"] = []
        return course

    soup = BeautifulSoup(res.text, "lxml")
    table = soup.find("table", id="StudentAttendanceDetailDataTable")

    attended_list = []

    if table:
        for tr in table.find_all("tr")[1:]:
            td = tr.find_all("td")

            attended_list.append({
                "Sl.No.": td[0].get_text(strip=True),
                "Date": td[1].get_text(strip=True),
                "Slot": td[2].get_text(strip=True),
                "Day / Time": td[3].get_text(strip=True),
                "Status": td[4].get_text(strip=True),
                "Remarks": td[5].get_text(strip=True),
            })
    else:
        print(f"Attendance table not found for {course['course_id']}")

    course["attended_list"] = attended_list

    course.pop("semester_id", None)
    course.pop("reg_no", None)
    course.pop("course_id_arg", None)
    course.pop("course_type_arg", None)

    return course


async def fetching_attendance(html_src, CSRF, client, vtop_engine):
    soup = BeautifulSoup(html_src, "lxml")

    table = soup.find("table", id="AttendanceDetailDataTable")

    if table is None:
        print("Attendance table not found.")
        return

    cookies = httpx.Cookies()
    cookies.set("JSESSIONID", vtop_engine)

    courses = []

    for tr in table.find_all("tr")[1:]:
        td = tr.find_all("td")

        course_text = td[2].get_text(" ", strip=True)

        course_id, course_name, course_type = map(
            str.strip,
            course_text.split(" - ", 2),
        )

        faculty = td[4].get_text(strip=True).split("-")[0]
        attended = td[5].get_text(strip=True)
        total = td[6].get_text(strip=True)
        percentage = td[7].get_text(strip=True)
        debar = td[8].get_text(strip=True)

        onclick = td[9].find("a")["onclick"]

        semester_id, reg_no, cid, ctype = (
            onclick.split("callStudentAttendanceDetailDisplay(")[1]
            .split(")")[0]
            .replace("'", "")
            .split(",")
        )

        courses.append({
            "course_id": course_id,
            "course_name": course_name,
            "course_type": course_type,
            "faculty": faculty,
            "attended": attended,
            "total": total,
            "percentage": percentage,
            "debar": debar,
            "semester_id": semester_id,
            "reg_no": reg_no,
            "course_id_arg": cid,
            "course_type_arg": ctype,
        })

    semaphore = asyncio.Semaphore(10)

    async def limited_fetch(course):
        async with semaphore:
            return await fetch_course(
                client,
                cookies,
                CSRF,
                course,
            )

    data = await asyncio.gather(
        *(limited_fetch(course) for course in courses)
    )

    with open(INFO, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
