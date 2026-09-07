from enpoints import EXAM_SCHEDULE
from services.EXAMSCHEDULE.parser import parse_schedule
from src.session import build_cookies
import httpx

async def get_schedule(client,vtop_engine,data4):

    r=await client.post(EXAM_SCHEDULE,cookies=build_cookies(vtop_engine),data=data4)
    parse_schedule(r.text)