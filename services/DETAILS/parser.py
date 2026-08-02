from bs4 import BeautifulSoup
from pathlib import Path
import json
ROOT_DIR=Path(__file__).resolve().parent.parent.parent
student_info=ROOT_DIR/"config"/"student_info.json"
def parse_details(html_src):
    soup=BeautifulSoup(html_src,"lxml")
    table=soup.find_all("table")
    #Student Details
    rows_1=table[0].find_all("tr")
    rows_2=table[4].find_all("tr")
    application_number=rows_1[0].find_all('td')[1].get_text(strip=True)
    student_name=rows_1[1].find_all('td')[1].get_text(strip=True)
    gender=rows_1[3].find_all('td')[1].get_text(strip=True)
    mobile_number=rows_1[14].find_all('td')[1].get_text(strip=True)
    parent_mobile=rows_1[-1].find_all('td')[1].get_text(strip=True)
    hostel_block=rows_2[2].find_all('td')[1].get_text(strip=True).split(" ")[0]
    room_number=rows_2[-3].find_all('td')[1].get_text(strip=True)

    #Procter Information 
    rows_3=table[3].find_all("tr")
    faculty_id = rows_3[0].find_all('td')[1].get_text(strip=True)
    faculty_name = rows_3[1].find_all('td')[1].get_text(strip=True)
    faculty_designation = rows_3[2].find_all('td')[1].get_text(strip=True)
    school = rows_3[3].find_all('td')[1].get_text(strip=True)
    cabin = rows_3[4].find_all('td')[1].get_text(strip=True)
    faculty_department = rows_3[5].find_all('td')[1].get_text(strip=True)
    faculty_email = rows_3[6].find_all('td')[1].get_text(strip=True)
    faculty_intercom = rows_3[7].find_all('td')[1].get_text(strip=True)
    faculty_mobile_number = rows_3[8].find_all('td')[1].get_text(strip=True)

    data = {
        "student_details": {
            "application_number": application_number,
            "student_name": student_name,
            "gender": gender,
            "mobile_number": mobile_number,
            "parent_mobile": parent_mobile,
            "hostel_block": hostel_block,
            "room_number": room_number
        },
        "proctor_information": {
            "faculty_id": faculty_id,
            "faculty_name": faculty_name,
            "faculty_designation": faculty_designation,
            "school": school,
            "cabin": cabin,
            "faculty_department": faculty_department,
            "faculty_email": faculty_email,
            "faculty_intercom": faculty_intercom,
            "faculty_mobile_number": faculty_mobile_number
        }
    }

    student_info.parent.mkdir(parents=True, exist_ok=True)

    with open(student_info, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


