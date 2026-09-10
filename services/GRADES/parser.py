import httpx
import re
import json
import asyncio
import logging
from pathlib import Path
from bs4 import BeautifulSoup
from enpoints import GRADES_DETAILS
from src.session import build_cookies
from email.utils import formatdate# import aiohttp

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
html_g=ROOT_DIR / "data"/"cache"/"html_g.html"
grades=ROOT_DIR / "config"/"grades.json"

logger=logging.getLogger(__name__)

async def fetch_grades(html_src,client,vtop_engine,csrf,semsub_id,username):
    try:
        soup=BeautifulSoup(html_src,"lxml")

        table=soup.find("table")
        if not table:
            logger.error("No grades table found")
            return
        
        data=[]
        codes=[]
        rows=table.find_all("tr")

        for row in rows[2:]:

            td=row.find_all("td")

            if len(td) < 8:
                logger.error("Invalid grades row found")
                continue    

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

            button = td[7].find("button")

            if not button:
                logger.error(f"No details button for {course_code}")
                codes.append(None)
                continue

            onclick_text = td[7].find("button")["onclick"]
            match = re.search(r"AM_[A-Za-z0-9_]+", onclick_text)

            if not match:
                logger.error(f"Could not find course ID for {course_code}")
                codes.append(None)
                continue

            codes.append(match.group())
    except Exception as e:
        logger.error(f"Failed to parse grades page: {e}")


    semaphore = asyncio.Semaphore(5)
    async def fetch_mark(client, payload):
        async with semaphore:
            try:
                resp = await client.post(
                    GRADES_DETAILS,
                    data=payload,
                    cookies=build_cookies(vtop_engine)
                )
                return resp.text
            except Exception as e:
                logger.error(
                    f"Unexpected error for {payload['courseId']}: {e}"
                )
                return None
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
            logger.error("Failed to fetch grades data")
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
    logger.info("Grades successfully saved")