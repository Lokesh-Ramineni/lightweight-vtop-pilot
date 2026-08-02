from enpoints import EXAM_SCHEDULE
from services.EXAMSCHEDULE.parser import parse_schedule
import httpx

async def get_schedule(client,vtop_engine,data4):
    ck = httpx.Cookies()
    ck.set("JSESSIONID", vtop_engine)
    r=await client.post(EXAM_SCHEDULE,cookies=ck,data=data4)
    parse_schedule(r.text)