from bs4 import BeautifulSoup
import re
import json
import asyncio
from email.utils import formatdate# import aiohttp
import httpx
from pathlib import Path
from enpoints import GRADES_DETAILS
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
html_g=ROOT_DIR / "data"/"cache"/"html_g.html"
grades=ROOT_DIR / "config"/"grades.json"
async def fetch_grades(html_src,client,vtop_engine,csrf,semsub_id,username):
    print('working')
    soup=BeautifulSoup(html_src,"lxml")

    table=soup.find("table")
    if not table:
        print("No data")
        return
    data=[

    ]
    codes=[]
    rows=table.find_all("tr")
    for row in rows[2:]:
        td=row.find_all("td")
        course_code=td[1].get_text(strip=True)
        course_title=td[2].get_text(strip=True)
        course_type=td[3].get_text(strip=True)
        grading_type=td[4].get_text(strip=True)
        grand_total=td[5].get_text(strip=True)
        grade=td[6].get_text(strip=True)

        data.append({
            "course_code":course_code,
            "course_title":course_title,
            "course_type":course_type,
            "grand_total":grand_total,
            "grade":grade,
            "grading_type":grading_type,
            "post":[]
        })

        onclick_text = td[7].find("button")["onclick"]
        match = re.search(r"AM_[A-Za-z0-9_]+", onclick_text)
        codes.append(match.group())


    semaphore = asyncio.Semaphore(5)
    ck = httpx.Cookies()
    ck.set("JSESSIONID", vtop_engine)
    async def fetch_mark(client, payload):
        async with semaphore:
            resp = await client.post(
                GRADES_DETAILS,
                data=payload,
                cookies=ck
            )
            return resp.text

    payload = {
        "authorizedID": username,
        "x":formatdate(timeval=None, localtime=False, usegmt=True),
        "semesterSubId": semsub_id,
        "courseId": "",
        "_csrf": csrf
    }
    tasks = [
        fetch_mark(client, {**payload,"courseId": code})
        for code in codes
    ]
    results = await asyncio.gather(*tasks,return_exceptions=True)

    for course, result in zip(data, results):
        if isinstance(result, Exception):
            print(f"Failed for {course['course_code']}: {result}")
            continue

        soup = BeautifulSoup(result, "lxml")
        table = soup.select("table.table-striped.table-bordered")[0]
        if not table:
            print("Failed to fetch data")
            return
        for tr in table.find_all("tr")[2:3]:
            class_strength=tr.find_all("td")[0].get_text(strip=True)
            grading_strength=tr.find_all("td")[1].get_text(strip=True)
            mean=tr.find_all("td")[2].get_text(strip=True)
            sd=tr.find_all("td")[3].get_text(strip=True)
            s=tr.find_all("td")[4].get_text(strip=True)
            a=tr.find_all("td")[5].get_text(strip=True)
            b=tr.find_all("td")[6].get_text(strip=True)
            c=tr.find_all("td")[7].get_text(strip=True)
            d=tr.find_all("td")[8].get_text(strip=True)
            e=tr.find_all("td")[9].get_text(strip=True)
            f=tr.find_all("td")[10].get_text(strip=True)

            course["post"].append({
                "class_strength":class_strength,
                "grading_strength":grading_strength,
                "mean":mean,
                "sd":sd,
                "s":s,
                "a":a,
                "b":b,
                "c":c,
                "d":d,
                "e":e,
                "f":f
            })


    grades.parent.mkdir(parents=True, exist_ok=True)
    with open(grades, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)