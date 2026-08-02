import asyncio
import os
import time
from email.utils import formatdate
from pathlib import Path
from dotenv import load_dotenv

from main import VtopClient
from services.TIMETABLE.service import time_table
from services.ATTENDANCE.service import attendance_table
from services.EXAMSCHEDULE.service import get_schedule
from services.semesters import semester_code
from services.DETAILS.service import get_details
import time
import httpx
import json
from bs4 import BeautifulSoup

env_path = Path.cwd() / "config" / ".env"
load_dotenv(env_path)

ROOT = Path(__file__).parent
sem_data = ROOT / "data" /"cache"/ "sem.html"
weekend=sem_data = ROOT / "data" /"cache"/ "weekend.html"
sem_codes=ROOT / "config"/ "sem_code.json"
details=ROOT/"config"/"student_info.json"
with open(sem_codes,"r") as f:
    s=json.load(f)

with open(details,"r") as f:
    d=json.load(f)

class Main:

    def __init__(self):
        self.username = os.environ.get("VTOP_USERNAME")
        self.semester = os.environ.get("SEMESTER")
        self.room=d["student_details"]["room_number"]
        self.name=d["student_details"]["student_name"]
        self.gender=d["student_details"]["gender"]
        self.hostel=d["student_details"]["hostel_block"]
        self.student=d["student_details"]["mobile_number"]
        self.parent=d["student_details"]["parent_mobile"]
        self.app=d["student_details"]["application_number"]

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

        flat_map = {}
        for item in s:
            flat_map.update(item)
        semester_names = list(flat_map.keys())

        # 2. Compact CLI Presentation (No extra print statements or newlines)
        print("Choose Semester:")
        for index, name in enumerate(semester_names, start=1):
            # strip() removes accidental whitespace padding from strings
            print(f" {index}. {name.strip()}")

        # 3. Direct Input line
        while True:
            try:
                choice = int(input("Enter the number: "))
                if 1 <= choice <= len(semester_names):
                    opted = semester_names[choice - 1]
                    break
                print("Invalid choice.")
            except ValueError:
                print("Enter digits only.")

        
        self.data1 = {
            "verifyMenu": "true",
            "authorizedID": str(self.username),
            "_csrf": self.csrf,
            "nocache": int(round(time.time() * 1000))
        }

        self.data2 = {
            "_csrf": self.csrf,
            "semesterSubId": flat_map[opted],
            "authorizedID": str(self.username),
            "x": formatdate(timeval=None, localtime=False, usegmt=True)
        }
        self.data3 = {
            "authorizedID": self.username,
            "BookingId": "",
            "regNo": self.username,
            "name":self.name,
            "applicationNo": self.app,
            "gender": self.gender,
            "hostelBlock": self.hostel,
            "roomNo": self.room,
            "outPlace": "",
            "purposeOfVisit": "",
            "outingDate": "",
            "outTime": "9:30 AM- 3:30PM",
            "contactNumber": self.student,
            "parentContactNumber": self.parent,
            "_csrf": self.csrf,
            "x": formatdate(timeval=None, localtime=False, usegmt=True),
        }

        self.data4={
            "authorizedID":self.username,
            "semesterSubId": flat_map[opted],
            "_csrf":self.csrf
        }

        return self

    async def main(self):

        await get_details(self.client,self.cookie,self.data1)
        await get_schedule(self.client,self.cookie,self.data4)

        await asyncio.gather(
            time_table(
                self.client,
                self.cookie,
                self.data1,
                self.data2
            ),
            attendance_table(
                self.client,
                self.cookie,
                self.data1,
                self.data2
            ),
            # semester_code(
            #     self.client,
            #     self.cookie,
            #     self.data1
            # )
        )
        # await semester_code(self.client,self.cookie,self.data1)
async def runner():
    start=time.time()
    m = await Main.create()
    await m.main()
    end=time.time()
    tot=end-start
    print(f'{tot:.4f}')


if __name__ == "__main__":
    asyncio.run(runner())
