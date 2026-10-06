# lightweight-vtop-pilot

A lightweight, async VTOP (VIT-AP) automation client built on `httpx`. It logs in without a browser, solves the captcha locally with a bundled model, fetches the login OTP from Gmail over IMAP, reuses saved sessions, and pulls your academic data (timetable, attendance, marks, grades, exam schedule and more) in parallel.

---

## Features

- Browser-less login using plain HTTP requests (`httpx`, async)
- Offline captcha solver (NumPy weights in `Weights/`, no external API)
- Automatic OTP retrieval from Gmail via IMAP
- Session reuse through a saved `JSESSIONID` (skips login when still valid)
- Concurrent fetching of all services with `asyncio.gather`
- Rotating log file (`logs/app.log`, 10 MB x 5 backups)

### Services

| Service | What it fetches |
|---|---|
| `TIMETABLE` | Weekly timetable for the chosen semester |
| `ATTENDANCE` | Course-wise attendance and details |
| `EXAMSCHEDULE` | Exam schedule |
| `MARKS` | Marks for the chosen semester |
| `GRADES` | Semester grades |
| `GRADE_HISTORY` | Complete grade history |
| `DETAILS` | Student profile (saved to `config/student_info.json`) |
| `BIOMETRIC` | Biometric attendance history |
| `OUTING` | Hostel outing form submission (work in progress, parser is empty) |
| `semesters.py` | Semester list (saved to `config/sem_code.json`) |

---

## Folder Structure

```
lightweight-vtop-pilot/
├── api/
│
├── captcha/
│   ├── .gitkeep
│   └── captcha.png
│
├── checks/
│   ├── content_check.py
│   └── prelogin_check.py
│
├── config/
│   ├── .env
│   ├── session.json
│   ├── sem_code.json
│   └── student_info.json
│
├── data/
│   └── cache/
│       ├── .gitkeep
│       ├── attendance.html
│       ├── captcha.html
│       ├── chech.html
│       ├── content.html
│       ├── exam.html
│       ├── html_g.html
│       ├── marks.html
│       ├── otp.html
│       ├── sem.html
│       ├── time.html
│       ├── timetable.html
│       └── weekend.html
│
├── logs/
│   ├── .gitkeep
│   └── app.log
│
├── services/
│   ├── ATTENDANCE/
│   │   ├── parser.py
│   │   └── service.py
│   ├── BIOMETRIC/
│   │   ├── parser.py
│   │   └── service.py
│   ├── DETAILS/
│   │   ├── parser.py
│   │   └── service.py
│   ├── EXAMSCHEDULE/
│   │   ├── parser.py
│   │   └── service.py
│   ├── GRADE_HISTORY/
│   │   ├── parser.py
│   │   └── service.py
│   ├── GRADES/
│   │   ├── parser.py
│   │   └── service.py
│   ├── MARKS/
│   │   ├── parser.py
│   │   └── service.py
│   ├── OUTING/
│   │   ├── outing.py
│   │   └── parser.py
│   ├── TIMETABLE/
│   │   ├── parser.py
│   │   └── service.py
│   └── semesters.py
│
├── src/
│   ├── get_captcha.py
│   ├── get_client.py
│   ├── get_csrf.py
│   ├── get_otp.py
│   ├── login_check.py
│   ├── otp_fetch.py
│   ├── post_prelog.py
│   ├── prelogin.py
│   ├── saving_cookies.py
│   ├── session.py
│   └── solve_cap.py
│
├── Weights/
│   ├── captcha_weights.npz
│   └── labels.json
│
├── .gitignore
├── enpoints.py
├── logging_config.py
├── main.py
├── pyproject.toml
├── README.md
├── requirements.txt
├── run.py
└── uv.lock
```

> `config/.env`, `session.json`, `sem_code.json` and `student_info.json` are git-ignored. `.env` you create yourself; the other three are generated automatically (see below). The `.idea/` and `.git/` folders are omitted from the tree.

### What each part does

| Path | Purpose |
|---|---|
| `main.py` | `VtopClient`: the full login flow (session check, prelogin, captcha, login, OTP) |
| `run.py` | Entry point: logs in, asks for a semester, runs all services concurrently |
| `enpoints.py` | All VTOP URLs and request headers |
| `logging_config.py` | Console and rotating-file logging setup |
| `src/` | Login building blocks: HTTP client, CSRF, captcha fetch and solve, OTP, cookies |
| `checks/` | Response validators for the prelogin and content pages |
| `services/` | One folder per feature, each with a `service.py` (request) and `parser.py` (HTML to data) |
| `Weights/` | Captcha model weights and labels |
| `config/` | Credentials (`.env`) and session/state JSON files |
| `data/cache/` | Raw HTML responses saved for debugging |
| `captcha/` | Latest downloaded captcha image |
| `logs/` | Application logs |
| `api/` | Reserved for a future API layer (currently empty) |

---

## Requirements

- Python **3.14 or newer** (`requires-python = ">=3.14"` in `pyproject.toml`)
- A VTOP (VIT-AP) account
- A Gmail account that receives the VTOP OTP emails, with an **App Password**
- [`uv`](https://docs.astral.sh/uv/) (recommended) or `pip`

Dependencies: `aiofiles`, `beautifulsoup4`, `httpx`, `lxml`, `numpy`, `pillow`, `python-dotenv`, `scipy`.

---

## Setup

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd lightweight-vtop-pilot
```

### 2. Install dependencies

**Using uv (recommended):**

```bash
uv sync
```

**Using pip:**

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Create the config folder and `.env`

```bash
mkdir -p config
```

Create `config/.env`:

```env
VTOP_USERNAME=your_registration_number
VTOP_PASSWORD=your_vtop_password
SEMESTER=your_semester_code

EMAIL=your_gmail_address@gmail.com
APP_PASSWORD=your_gmail_app_password
```

| Variable | Description |
|---|---|
| `VTOP_USERNAME` | Your VTOP registration number |
| `VTOP_PASSWORD` | Your VTOP password |
| `SEMESTER` | Semester identifier |
| `EMAIL` | Gmail address that receives VTOP OTP emails |
| `APP_PASSWORD` | Gmail App Password (not your normal password) |

### 4. Set up the Gmail App Password (for OTP)

1. Enable 2-Step Verification on your Google account.
2. Go to **Google Account > Security > App passwords**.
3. Generate a password and paste it as `APP_PASSWORD`.
4. Make sure IMAP is enabled in Gmail settings.
5. The script looks for emails from `noreply.sdc@vitap.ac.in` with the subject `VTOP Login OTP Needed`.

### 5. Prepare the generated config files (important)

`run.py` reads `config/sem_code.json` and `config/student_info.json` when it starts, and both are created by the services themselves (`semesters.py` and `DETAILS`). On a **fresh clone they do not exist, so the first run will fail** with a `FileNotFoundError`.

To get past this once, create them as empty placeholders:

```bash
echo "[]" > config/sem_code.json
echo '{"student_details": {"room_number": "", "student_name": "", "gender": "", "hostel_block": "", "mobile_number": "", "parent_mobile": "", "application_number": ""}}' > config/student_info.json
```

Run the script once. Both files get overwritten with real data. The semester list will be empty on that first run, so run it a second time to pick a semester. Alternatively, run `python main.py` first: it only does the login flow and does not need those files.

---

## Usage

```bash
# with uv
uv run run.py

# or with plain Python
python run.py
```

What happens:

1. Loads a saved session from `config/session.json`; if it is still valid, login is skipped.
2. Otherwise it logs in: fetches the captcha, solves it locally, submits credentials, and fetches the OTP from Gmail if VTOP asks for one.
3. Shows a semester menu:
   ```
   Choose Semester:
    1. ...
    2. ...
   Enter the number:
   ```
4. Fetches timetable, attendance, exam schedule, marks, grades, grade history, student details and biometric data concurrently.
5. Prints the total time taken.

To test only the login flow:

```bash
python main.py
```

### Output and logs

- Application logs: `logs/app.log`
- Captcha image: `captcha/captcha.png`
- Cached raw HTML: `data/cache/`

---

## Notes and Limitations

- **Outing:** `services/OUTING` is not wired into `run.py`, and its parser is empty. `run.py` also contains hard-coded values (e.g. `fromDate` and the outing time slot) that you should change for your own use.
- **Login retries:** `VtopClient(login_tries=1)` makes one login attempt by default. Captcha failures are retried up to 10 times inside that attempt.
- **OTP timeout:** the OTP fetcher waits up to 60 seconds for the email.
- **Sectigo certificate:** `src/get_client.py` embeds a Sectigo CA certificate so the `httpx` client can verify the VTOP server.

---

## Security

- Never commit `config/.env`, `config/session.json` or any other file in `config/`. They are already covered by `.gitignore`.
- Use a Gmail **App Password**, never your real Google password.
- Treat `session.json` like a password: anyone holding the `JSESSIONID` can access your VTOP account.

---

## Disclaimer

This project is for personal and educational use. It is not affiliated with or endorsed by VIT. Use it responsibly and in line with your institution's policies.