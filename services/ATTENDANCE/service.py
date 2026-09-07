from http import cookies
from src.session import build_cookies
from enpoints import ATTENDANCE_PRE,PROCESS_ATTENDANCE
from pathlib import Path
from services.ATTENDANCE.parser import fetching_attendance
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
timetable_path = ROOT_DIR / "data" / "cache"
import httpx
async def attendance_table(client,vtop_engine,data1,data2,username):

    r=await client.post(ATTENDANCE_PRE,cookies=build_cookies(vtop_engine),data=data1)
    s=await client.post(PROCESS_ATTENDANCE,data=data2,cookies=build_cookies(vtop_engine))

    await fetching_attendance(s.text,data1["_csrf"],client,vtop_engine,username)
    # with open(timetable_path/"attendance.html","wb") as f:
    #     f.write(s.content)