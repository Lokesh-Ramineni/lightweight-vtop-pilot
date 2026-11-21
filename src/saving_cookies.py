from pathlib import Path
from src.secure_io import write_private_json

ROOT_DIR = Path(__file__).parent.parent
session = ROOT_DIR / "config" / "session.json"


def save(session_id: str) -> None:
    write_private_json(session, {"JSESSIONID": session_id})