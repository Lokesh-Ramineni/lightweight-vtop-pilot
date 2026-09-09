import json 
import logging
from pathlib import Path  
from bs4 import BeautifulSoup
from enpoints import TIME_TABLE_PRE
from src.session import build_cookies

ROOT = Path(__file__).parent.parent
sem_data = ROOT / "data" /"cache"/ "sem.html"
sem_codes=ROOT / "config"/ "sem_code.json"

logger=logging.getLogger(__name__)

async def semester_code(client,vtop_engine,data1):
    logger.info("Requesting semesters data")
    try:
        r=await client.post(TIME_TABLE_PRE,cookies=build_cookies(vtop_engine),data=data1)
        r.raise_for_status()
    except Exception:
        logger.exception(f"Failed to fetch semester data")
        return
    logger.info("Request Successfull")
    soup=BeautifulSoup(r.text,"lxml")

    # with open(sem_data, "wb") as f:
    #     f.write(r.content)
    
    select=soup.find("select",id="semesterSubId")
    if select is None:
        logger.error("Semester select element not found")
        return

    data=[]
    for opt in select.find_all("option")[1:]:
        sem=opt.get_text(strip=True)
        sem_code=opt.get("value")
        data.append({
            sem:sem_code
        })

    sem_codes.parent.mkdir(parents=True, exist_ok=True)
    with open(sem_codes,"w",encoding="utf-8") as f:
        json.dump(data,f,indent=4)
    logger.info("Semester data Successfully saved")
        