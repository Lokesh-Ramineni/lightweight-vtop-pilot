from enpoints import GRADE_HISTORY
from services.GRADE_HISTORY.parser import fetch_grade_history
from src.session import build_cookies
import httpx
async def get_history(client,vtop_engine,data1):
    r=await client.post(GRADE_HISTORY,data=data1,cookies=build_cookies(vtop_engine))
    fetch_grade_history(r.text)