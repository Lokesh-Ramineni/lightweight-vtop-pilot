import asyncio
import os
import time
from email.utils import formatdate
from pathlib import Path
from dotenv import load_dotenv

from main import VtopClient
from services.TIMETABLE.service import time_table

env_path = Path.cwd() / "config" / ".env"
load_dotenv(env_path)


import asyncio
import os
import time
from email.utils import formatdate
from pathlib import Path
from dotenv import load_dotenv

from main import VtopClient
from services.TIMETABLE.service import time_table

env_path = Path.cwd() / "config" / ".env"
load_dotenv(env_path)


class Main:

    @classmethod
    async def create(cls):
        self = cls()

        bot = VtopClient()
        self.client, self.csrf, self.cookie = await bot.run_flow()

        return self

    async def main(self):
        username = os.environ.get("VTOP_USERNAME")
        semester = os.environ.get("SEMESTER")

        data1 = {
            "verifyMenu": "true",
            "authorizedID": str(username),
            "_csrf": self.csrf,
            "nocache": int(round(time.time() * 1000))
        }

        data2 = {
            "_csrf": self.csrf,
            "semesterSubId": str(semester),
            "authorizedID": str(username),
            "x": formatdate(timeval=None, localtime=False, usegmt=True)
        }

        await time_table(self.client, self.cookie, data1, data2)


async def runner():
    m = await Main.create()
    await m.main()


if __name__ == "__main__":
    asyncio.run(runner())
