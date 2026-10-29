import json
from config import DATA_DIR, SUBSCRIPTIONS_FILE


def initialize_storage():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    if not SUBSCRIPTIONS_FILE.exists():
        with SUBSCRIPTIONS_FILE.open("w", encoding="utf-8") as file:
            json.dump([], file, indent=4)


def load_subscriptions():
    initialize_storage()

    try:
        with SUBSCRIPTIONS_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)

        if isinstance(data, list):
            return data

        print("Warning: Subscription data must be a JSON list.")
        return []

    except (OSError, json.JSONDecodeError) as error:
        print(f"Could not load subscriptions: {error}")
        return []


def save_subscriptions(subscriptions):
    initialize_storage()

    with SUBSCRIPTIONS_FILE.open("w", encoding="utf-8") as file:
        json.dump(subscriptions, file, indent=4, ensure_ascii=False)
