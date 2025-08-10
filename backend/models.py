
# models.py
from datetime import date, datetime
import csv
import os
from typing import Dict, Any

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
LOG_FILE = os.path.join(DATA_DIR, 'drink_log.csv')
SETTINGS_FILE = os.path.join(DATA_DIR, 'settings.json')

import json

DEFAULT_SETTINGS = {
    "reminder_interval_minutes": 30,
    "stand_duration_minutes": 3,
    "stand_enabled": True,
    "goal_ml_basic": 1000,
    "goal_ml_full": 1500
}

os.makedirs(DATA_DIR, exist_ok=True)

# ensure log exists
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['date', 'water_ml'])

# ensure settings exists
if not os.path.exists(SETTINGS_FILE):
    with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
        json.dump(DEFAULT_SETTINGS, f, ensure_ascii=False, indent=2)


def _read_settings() -> Dict[str, Any]:
    with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def _write_settings(s: Dict[str, Any]):
    with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
        json.dump(s, f, ensure_ascii=False, indent=2)


def get_settings() -> Dict[str, Any]:
    return _read_settings()


def update_settings(new: Dict[str, Any]) -> Dict[str, Any]:
    s = _read_settings()
    s.update(new)
    _write_settings(s)
    return s


def _normalize_date_str(d: str) -> str:
    # Accepts yyyy-mm-dd or other common separators
    return datetime.fromisoformat(d).date().isoformat()


def load_today_ml() -> int:
    today = date.today().isoformat()
    try:
        with open(LOG_FILE, 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                if len(row) >= 2 and row[0] == today:
                    return int(row[1])
    except Exception:
        return 0
    return 0


def save_today_ml(amount: int):
    today = date.today().isoformat()
    rows = []
    try:
        with open(LOG_FILE, 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader, None)
            rows = list(reader)
    except FileNotFoundError:
        header = ['date', 'water_ml']
        rows = []

    normalized = []
    found = False
    for row in rows:
        if not row or len(row) < 2:
            continue
        rec_date = row[0]
        try:
            rec_date = _normalize_date_str(rec_date)
        except Exception:
            continue
        if rec_date == today:
            normalized.append([today, str(amount)])
            found = True
        else:
            normalized.append([rec_date, row[1]])
    if not found:
        normalized.append([today, str(amount)])

    with open(LOG_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['date', 'water_ml'])
        writer.writerows(normalized)


def get_history(days: int = 7):
    # return last N days (including today) as list of {date, water_ml}
    out = []
    try:
        with open(LOG_FILE, 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                if len(row) < 2: continue
                out.append({'date': row[0], 'water_ml': int(row[1])})
    except Exception:
        pass
    return out
