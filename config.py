from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
SUBSCRIPTIONS_FILE = DATA_DIR / "subscriptions.json"

DATE_FORMAT = "%Y-%m-%d"

BILLING_CYCLES = [
    "Weekly",
    "Monthly",
    "Quarterly",
    "Half-Yearly",
    "Yearly"
]

SUBSCRIPTION_STATUSES = ["Active", "Cancelled"]
