from http import cookies

from enpoints import TIME_TABLE_PRE,PROCESS_TABLE
from pathlib import Path
from services.TIMETABLE.parser import fetching_timetable
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
timetable_path = ROOT_DIR / "data" / "cache"
import httpx
async def time_table(client,vtop_engine,data1,data2):
    ck = httpx.Cookies()
    ck.set("JSESSIONID", vtop_engine)

    r=await client.post(TIME_TABLE_PRE,cookies=ck,data=data1)
    print(client.cookies)
    print(r.status_code)
    s=await client.post(PROCESS_TABLE,data=data2,cookies=ck)
    print(s.url)
    print(s.status_code)
    fetching_timetable(s.text)
    with open(timetable_path/"timetable.html","wb") as f:
        f.write(s.content)