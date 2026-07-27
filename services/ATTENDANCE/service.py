from http import cookies

from enpoints import ATTENDANCE_PRE,PROCESS_ATTENDANCE
from pathlib import Path
from services.ATTENDANCE.parser import fetching_attendance
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
timetable_path = ROOT_DIR / "data" / "cache"
import httpx
async def attendance_table(client,vtop_engine,data1,data2):
    ck = httpx.Cookies()
    ck.set("JSESSIONID", vtop_engine)

    r=await client.post(ATTENDANCE_PRE,cookies=ck,data=data1)
    print(client.cookies)
    print(r.status_code)
    s=await client.post(PROCESS_ATTENDANCE,data=data2,cookies=ck)
    print(s.url)
    print(s.status_code)
    await fetching_attendance(s.text,data1["_csrf"],client,vtop_engine)
    with open(timetable_path/"attendance.html","wb") as f:
        f.write(s.content)