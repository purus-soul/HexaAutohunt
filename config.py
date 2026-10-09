import os

from dotenv import load_dotenv

load_dotenv()

api_id_value = os.getenv("TELEGRAM_API_ID", "").strip()
api_hash = os.getenv("TELEGRAM_API_HASH", "").strip()
phone_number = os.getenv("TELEGRAM_PHONE_NUMBER", "").strip()
chat_value = os.getenv("TELEGRAM_GAME_CHAT", "").strip()

missing = [
    name
    for name, value in (
        ("TELEGRAM_API_ID", api_id_value),
        ("TELEGRAM_API_HASH", api_hash),
        ("TELEGRAM_PHONE_NUMBER", phone_number),
        ("TELEGRAM_GAME_CHAT", chat_value),
    )
    if not value
]
if missing:
    raise RuntimeError(
        "Missing settings in .env: " + ", ".join(missing)
    )

try:
    api_id = int(api_id_value)
except ValueError as exc:
    raise RuntimeError("TELEGRAM_API_ID must be an integer.") from exc

# TELEGRAM_GAME_CHAT can be a numeric chat ID or a username such as @HeXamonbot.
chat = int(chat_value) if chat_value.lstrip("-").isdigit() else chat_value

hunt_interval_seconds = float(os.getenv("HUNT_INTERVAL_SECONDS", "10"))
if hunt_interval_seconds < 3:
    raise ValueError("HUNT_INTERVAL_SECONDS must be at least 3 seconds.")
