from enpoints import GRADES_INFO
from services.GRADES.parser import fetch_grades
import httpx
async def get_grades(client,vtop_engine,data4,csrf,semsub_id,username):
    ck=httpx.Cookies()
    ck.set("JSESSIONID",vtop_engine)
    r=await client.post(GRADES_INFO,cookies=ck,data=data4)
    await fetch_grades(r.text,client,vtop_engine,csrf,semsub_id,username)
    print(r.status_code)