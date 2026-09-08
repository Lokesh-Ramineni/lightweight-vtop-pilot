import httpx
import logging
from pathlib import Path
from src.session import build_cookies
from enpoints import PROCESS_ATTENDANCE
from services.ATTENDANCE.parser import fetching_attendance

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
timetable_path = ROOT_DIR / "data" / "cache"

logger = logging.getLogger(__name__)

async def attendance_table(client,vtop_engine,data1,data2,username):
    try:
        s=await client.post(PROCESS_ATTENDANCE,data=data2,cookies=build_cookies(vtop_engine))
        s.raise_for_status()
        
        await fetching_attendance(s.text,data1["_csrf"],client,vtop_engine,username)
    except httpx.HTTPError as e:
        logger.error("Attendance request failed: %s", e)
        return None
    except Exception:
        logger.exception("Unexpected error while fetching attendance")
        return None
    
    # with open(timetable_path/"attendance.html","wb") as f:
    #     f.write(s.content)