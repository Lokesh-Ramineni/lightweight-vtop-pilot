from bs4 import BeautifulSoup
from enpoints import TIME_TABLE_PRE
from pathlib import Path  
import json  
import httpx

ROOT = Path(__file__).parent.parent
sem_data = ROOT / "data" /"cache"/ "sem.html"
sem_codes=ROOT / "config"/ "sem_code.json"

async def semester_code(client,vtop_engine,data1):
    ck = httpx.Cookies()
    ck.set("JSESSIONID", vtop_engine)

    r=await client.post(TIME_TABLE_PRE,cookies=ck,data=data1)
    soup=BeautifulSoup(r.text,"lxml")

    with open(sem_data, "wb") as f:
        f.write(r.content)
    
    select=soup.find("select",id="semesterSubId")
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
        print("success")
        