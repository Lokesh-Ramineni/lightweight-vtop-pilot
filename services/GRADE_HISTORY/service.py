from enpoints import GRADE_HISTORY
from services.GRADE_HISTORY.parser import fetch_grade_history
import httpx
async def get_history(client,vtop_engine,data1):
    ck=httpx.Cookies()
    ck.set("JSESSIONID",vtop_engine)
    r=await client.post(GRADE_HISTORY,data=data1,cookies=ck)
    fetch_grade_history(r.text)
    print(r.status_code)