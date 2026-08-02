from enpoints import STUDENT_DETAILS
from services.DETAILS.parser import parse_details
import httpx
async def get_details(client,vtop_engine,data1):
    ck = httpx.Cookies()
    ck.set("JSESSIONID", vtop_engine)
    r=await client.post(STUDENT_DETAILS,cookies=ck,data=data1)
    parse_details(r.text)