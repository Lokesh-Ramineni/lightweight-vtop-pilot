from bs4 import BeautifulSoup
import json
import logging
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
info = ROOT / "config" / "info.json"

logger = logging.getLogger(__name__)
def fetching_timetable(html_src):
    logger.info("Starting timetable parsing")
    data = []
    try:
        soup = BeautifulSoup(html_src, "lxml")

        table = soup.find("table", class_="table")
        table_time = soup.find("table", id="timeTableStyle")

        if table is None or table_time is None:
            logger.warning(
                "Timetable tables not found | main_table=%s | time_table=%s",
                table is not None,
                table_time is not None,
            )
            return

        table_rows = table_time.find_all("tr")
        trs = table.find_all("tr")

        for tr in trs[2:-2]:

            td = tr.find_all("td")

            course_text = td[2].find_all("p")[0].get_text(strip=True)
            course_id, course_name = map(
                str.strip,
                course_text.split(" - ", 1)
            )

            course_type = (
                td[2]
                .find_all("p")[1]
                .get_text(strip=True)
                .strip("()")
                .strip()
            )

            slot = (
                td[7]
                .find_all("p")[0]
                .get_text(strip=True)
                .replace("-", "")
                .strip()
            )

            room = td[7].find_all("p")[1].get_text(strip=True)

            faculty = (
                td[8]
                .find_all("p")[0]
                .get_text(strip=True)
                .replace("-", "")
                .strip()
            )

            data.append({
                "course_id": course_id,
                "course_name": course_name,
                "course_type": course_type,
                "slot": slot,
                "room": room,
                "faculty": faculty,
                "schedule": []
            })
        logger.info(
            "Courses extracted from timetable | count=%d",
            len(data),
        )
        add_schedule(data, table_rows)
        logger.info("Course schedules added successfully")
        info.parent.mkdir(parents=True, exist_ok=True)
        with open(info, "w",encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        logger.info("Timetable saved successfully")
    except Exception:
        logger.exception("Failed to process timetable")
        raise

def add_schedule(data, table_rows):

    logger.info(
        "Starting schedule processing | courses=%d",
        len(data),
    )
    schedule_count = 0
    theory_start = [
        td.get_text(strip=True)
        for td in table_rows[0].find_all("td")[2:]
    ]

    theory_end = [
        td.get_text(strip=True)
        for td in table_rows[1].find_all("td")[1:]
    ]

    lab_start = [
        td.get_text(strip=True)
        for td in table_rows[2].find_all("td")[2:]
    ]

    lab_end = [
        td.get_text(strip=True)
        for td in table_rows[3].find_all("td")[1:]
    ]

    days = [
        ("Tuesday", table_rows[4], table_rows[5]),
        ("Wednesday", table_rows[6], table_rows[7]),
        ("Thursday", table_rows[8], table_rows[9]),
        ("Friday", table_rows[10], table_rows[11]),
        ("Saturday", table_rows[12], table_rows[13]),
    ]

    for course in data:

        slots = course["slot"].split("+")

        is_lab = "Lab" in course["course_type"]

        for day, theory_row, lab_row in days:

            if is_lab:
                row = lab_row
                cells = row.find_all("td")[1:]      
                start_times = lab_start
                end_times = lab_end
            else:
                row = theory_row
                cells = row.find_all("td")[2:]      
                start_times = theory_start
                end_times = theory_end

            for col, cell in enumerate(cells):

                text = cell.get_text(" ", strip=True)

                if text in ("", "-", "--", "Lunch"):
                    continue

                for slot in slots:

                    if text.startswith(slot + "-"):

                        course["schedule"].append({
                            "day": day,
                            "slot": slot,
                            "start": start_times[col],
                            "end": end_times[col]
                        })
                        schedule_count += 1
    logger.info(
        "Schedule processing completed | schedules=%d",
        schedule_count,
    )