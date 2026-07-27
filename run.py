import asyncio
import os
import time
from email.utils import formatdate
from pathlib import Path
from dotenv import load_dotenv

from main import VtopClient
from services.TIMETABLE.service import time_table
from services.ATTENDANCE.service import attendance_table

env_path = Path.cwd() / "config" / ".env"
load_dotenv(env_path)


class Main:

    def __init__(self):
        self.username = os.environ.get("VTOP_USERNAME")
        self.semester = os.environ.get("SEMESTER")

        self.client = None
        self.csrf = None
        self.cookie = None

        self.data1 = None
        self.data2 = None

    @classmethod
    async def create(cls):
        self = cls()

        bot = VtopClient()
        self.client, self.csrf, self.cookie = await bot.run_flow()

        self.data1 = {
            "verifyMenu": "true",
            "authorizedID": str(self.username),
            "_csrf": self.csrf,
            "nocache": int(round(time.time() * 1000))
        }

        self.data2 = {
            "_csrf": self.csrf,
            "semesterSubId": str(self.semester),
            "authorizedID": str(self.username),
            "x": formatdate(timeval=None, localtime=False, usegmt=True)
        }

        return self

    async def main(self):

        await time_table(
            self.client,
            self.cookie,
            self.data1,
            self.data2
        )

        await attendance_table(
            self.client,
            self.cookie,
            self.data1,
            self.data2
        )
async def runner():
    m = await Main.create()
    await m.main()


if __name__ == "__main__":
    asyncio.run(runner())
