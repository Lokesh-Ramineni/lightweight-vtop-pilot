import json
import os
import asyncio
import aiofiles
import time
from pathlib import Path
from dotenv import load_dotenv
import httpx

from src.get_client import get_client
from src.get_csrf import get_csrf, get_csrf_token
from src.prelogin import get_prelogin
from src.get_captcha import get_captcha
from src.post_prelog import get_post_prelogin
from src.otp_fetch import OTPFetcher
from src.session import cookie_check
from src.saving_cookies import save
from src.get_otp import get_otp_pg, validate, redirect
from checks.prelogin_check import check
from src.login_check import login_ch
# from checks.content_check import cont_check

from enpoints import OPEN_PAGE,ERROR
import logging

env_path = Path.cwd() / "config" / ".env"
loaded = load_dotenv(env_path)

ROOT_DIR = Path(__file__).parent
cache = ROOT_DIR / "data" / "cache"
session = ROOT_DIR / "config" / "session.json"


logger = logging.getLogger(__name__)

class VtopClient:

    def __init__(self, login_tries=1):
        self.registration_number = os.getenv('VTOP_USERNAME')
        self.password = os.getenv('VTOP_PASSWORD')
        self.login_tries = login_tries

    async def run_flow(self):
        print(f'Flow Initiated...')

        
        client = get_client()
        session_check = False

        for _ in range(0,self.login_tries):

            # Trying to open initial page and get the csrf_token
            cookie=None
            html_src=None
            try:
                async with aiofiles.open(session, "r") as f:
                    content = await f.read()
                    load_cookie = json.loads(content)
                cookie = load_cookie["JSESSIONID"]
                print(f'cookies: {cookie}')

                r, u = await cookie_check(client, cookie)

                #Add the check state
                #pending

                if r.status_code == 200 and "login" not in str(u).lower():
                    logger.info("Session is active")
                    session_check = True

                    # with open(cache / "content.html", "wb") as f:
                    #     f.write(r.content)

                    return client, get_csrf_token(r.text),cookie
                else:
                    logger.info(f'session check failed, creating new..')

            except Exception as e:
                print(f'Cookie not found: {e}')

            if not session_check:

                try:
                    request = await client.get(
                        url=OPEN_PAGE)
                    print(f'/open/login Status Code: {request.status_code}')

                    # Fetching csrf_token
                    csrf_token, flag_value = get_csrf(request.text)

                    prelog_data = {
                        '_csrf': csrf_token,
                        "flag": flag_value
                    }

                    # Fetching Captcha
                    i=0
                    while i<10:
                        # PreLogin Session
                        prelog = await get_prelogin(client, prelog_data)
                        if check(prelog.text) is not True:
                            logger.info(f'/vtop/prelogin/setup prelogin failed: {prelog.status_code}')
                            # with open(cache / "captcha.html", "wb") as f:
                            #     f.write(prelog.content)
                        else:
                            logger.info(f'/vtop/prelogin/setup prelogin success: {prelog.status_code}')

                        new_client, html_src,text = await get_captcha(prelog.text,client)
                        new_csrf_token = get_csrf_token(html_src)

                        # Post PreLogin
                        postlog_data = {
                            '_csrf': new_csrf_token,
                            "username": self.registration_number,
                            "password": self.password,
                            "captchaStr": text
                        }

                        postprelog = await get_post_prelogin(new_client, postlog_data)
                        i+=1
                        if not login_ch(postprelog.text) and postprelog.url != ERROR:
                            break


                    # Otp Check
                    ses = True
                    if postprelog.url == ERROR:
                        otp_log = await get_otp_pg(client)
                        logger.info("Otp detected")
                        otp_csrf_token = get_csrf_token(otp_log.text)
                        get_otp = OTPFetcher()
                        val = get_otp.fetch_latest_otp(60)
                        data = {
                            "otpCode": val,
                            "_csrf": otp_csrf_token
                        }
                        logger.info(f'Fetched Otp: {val}')

                        cont = await validate(client, data)
                        # with open(cache / "otp.html", "wb") as f:
                        #     f.write(otp_log.content)

                        next_page = await redirect(client, cont.json()["redirectUrl"])
                        save(client.cookies)
                        ses = False
                        # with open(cache / "captcha.html", "wb") as f:
                        #     f.write(next_page.content)
                        # print(next_page.status_code)
                        return client, get_csrf_token(next_page.text),cookie

                    if ses:
                        save(client.cookies)
                        # with open(cache / "captcha.html", "wb") as f:
                        #     f.write(postprelog.content)
                        return client, get_csrf_token(postprelog.text),cookie

                except Exception as e:
                    logger.error(f'Failed to login: {e}')

                if html_src is not None:
                    return client, get_csrf_token(html_src),cookie
                return client, None
        return None

async def start():
    bot = VtopClient()
    await bot.run_flow()


if __name__ == "__main__":
    asyncio.run(start())