from enpoints import STUDENT_DETAILS
from services.DETAILS.parser import parse_details
from src.session import build_cookies
import httpx
async def get_details(client,vtop_engine,data1):
    r=await client.post(STUDENT_DETAILS,cookies=build_cookies(vtop_engine),data=data1)
    parse_details(r.text)