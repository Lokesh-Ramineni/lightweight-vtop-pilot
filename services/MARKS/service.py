from enpoints import MARKS_INFO
from services.MARKS.parser import fetch_marks
from pathlib import Path
import httpx
ROOT_DIR=Path(__file__).resolve().parent.parent.parent

timetable_path = ROOT_DIR / "data" / "cache"
async def get_marks(client,vtop_engine,data4):
    ck=httpx.Cookies()
    ck.set("JSESSIONID", vtop_engine)
    r=await client.post(MARKS_INFO,data=data4,cookies=ck)
    fetch_marks(r.text)
    print(r.status_code)
    with open(timetable_path/"marks.html","wb") as f:
        f.write(r.content)