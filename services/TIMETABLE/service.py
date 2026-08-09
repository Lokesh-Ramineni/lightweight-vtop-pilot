# from http import cookies
import httpx
import logging
from pathlib import Path
from logging_config import setup_logging

from enpoints import TIME_TABLE_PRE,PROCESS_TABLE
from services.TIMETABLE.parser import fetching_timetable



ROOT_DIR = Path(__file__).resolve().parent.parent.parent
timetable_path = ROOT_DIR / "data" / "cache"

logger = logging.getLogger(__name__)

async def time_table(client,vtop_engine,data1,data2):
    ck = httpx.Cookies()
    ck.set("JSESSIONID", vtop_engine)

    # r=await client.post(TIME_TABLE_PRE,cookies=ck,data=data1)
    logger.info("Requesting timetable")
    try:
        s=await client.post(PROCESS_TABLE,data=data2,cookies=ck)
        logger.info("Requesting success")
        fetching_timetable(s.text)
    except Exception as e:
        logger.error("Requesting timetable failed",e)
    # with open(timetable_path/"timetable.html","wb") as f:
    #     f.write(s.content)