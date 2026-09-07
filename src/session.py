from enpoints import CONTENT
import httpx
async def cookie_check(client,cookie):

    chk=await client.get(CONTENT,cookies=build_cookies(cookie))
    return chk,str(chk.url)


def build_cookies(sessionid: str) -> httpx.Cookies:
    cookies = httpx.Cookies()
    cookies.set("JSESSIONID", sessionid)
    return cookies