
# services.py
from models import load_today_ml, save_today_ml, get_settings, update_settings


# business functions used by API

def get_status():
    settings = get_settings()
    current = load_today_ml()
    return {
        "water_ml": current,
        **settings
    }


def add_water(amount: int) -> dict:
    if not isinstance(amount, int):
        raise ValueError("amount must be int")
    cur = load_today_ml()
    cur = max(0, cur + amount)
    save_today_ml(cur)
    return get_status()


def reset_water() -> dict:
    save_today_ml(0)
    return get_status()


def set_settings(reminder_interval: float = None, stand_duration: int = None, stand_enabled: bool = None):
    new = {}
    if reminder_interval is not None:
        new['reminder_interval_minutes'] = float(reminder_interval)
    if stand_duration is not None:
        new['stand_duration_minutes'] = stand_duration
    if stand_enabled is not None:
        new['stand_enabled'] = bool(stand_enabled)
    updated = update_settings(new)
    return {**get_status(), **updated}
