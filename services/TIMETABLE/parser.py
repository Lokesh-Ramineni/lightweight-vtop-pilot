from bs4 import BeautifulSoup
import json
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
info = ROOT / "config" / "info.json"


def fetching_timetable(html_src):
    data = []

    soup = BeautifulSoup(html_src, "html.parser")

    table = soup.find("table", class_="table")
    table_time = soup.find("table", id="timeTableStyle")

    if table is None or table_time is None:
        print("Table not found")
        return

    table_rows = table_time.find_all("tr")

    # ----------------------------
    # COURSE TABLE
    # ----------------------------
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

    add_schedule(data, table_rows)

    with open(info, "w") as f:
        json.dump(data, f, indent=4)

    print("Saved to", info)


def add_schedule(data, table_rows):

    # ----------------------------
    # THEORY TIME HEADER
    # ----------------------------
    theory_start = [
        td.get_text(strip=True)
        for td in table_rows[0].find_all("td")[2:]
    ]

    theory_end = [
        td.get_text(strip=True)
        for td in table_rows[1].find_all("td")[1:]
    ]

    # ----------------------------
    # LAB TIME HEADER
    # ----------------------------
    lab_start = [
        td.get_text(strip=True)
        for td in table_rows[2].find_all("td")[2:]
    ]

    lab_end = [
        td.get_text(strip=True)
        for td in table_rows[3].find_all("td")[1:]
    ]

    # ----------------------------
    # DAY ROWS
    # ----------------------------
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
                cells = row.find_all("td")[1:]      # LAB row has no DAY column
                start_times = lab_start
                end_times = lab_end
            else:
                row = theory_row
                cells = row.find_all("td")[2:]      # THEORY row has DAY + THEORY
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


if __name__ == "__main__":

    with open("timetable.html", encoding="utf-8") as f:
        html = f.read()

    fetching_timetable(html)