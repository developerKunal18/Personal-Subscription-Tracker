from collections import Counter

from storage import load_subscriptions
from utils import days_until, next_billing_date


def monthly_cost(subscription):
    amount = float(subscription.get("amount", 0))
    cycle = subscription.get("billing_cycle")

    multipliers = {
        "Weekly": 52 / 12,
        "Monthly": 1,
        "Quarterly": 1 / 3,
        "Half-Yearly": 1 / 6,
        "Yearly": 1 / 12
    }

    return amount * multipliers.get(cycle, 0)


def yearly_cost(subscription):
    return monthly_cost(subscription) * 12


def spending_report():
    subscriptions = load_subscriptions()

    active = [
        item for item in subscriptions
        if item.get("status") == "Active"
    ]

    monthly_total = sum(monthly_cost(item) for item in active)
    yearly_total = sum(yearly_cost(item) for item in active)

    print("\n========== SUBSCRIPTION SPENDING ==========")
    print(f"Total subscriptions : {len(subscriptions)}")
    print(f"Active              : {len(active)}")
    print(
        f"Cancelled           : "
        f"{sum(1 for item in subscriptions if item.get('status') == 'Cancelled')}"
    )
    print(f"Estimated monthly   : ₹{monthly_total:.2f}")
    print(f"Estimated yearly    : ₹{yearly_total:.2f}")
    print("=" * 43)


def provider_report():
    subscriptions = load_subscriptions()

    active = [
        item for item in subscriptions
        if item.get("status") == "Active"
    ]

    if not active:
        print("No active subscriptions available.")
        return

    totals = {}

    for item in active:
        provider = item.get("provider", "Unknown")
        totals[provider] = totals.get(provider, 0) + monthly_cost(item)

    print("\n--- Estimated Monthly Cost by Provider ---")

    for provider, amount in sorted(totals.items()):
        print(f"{provider}: ₹{amount:.2f}")


def billing_cycle_report():
    subscriptions = load_subscriptions()

    active = [
        item for item in subscriptions
        if item.get("status") == "Active"
    ]

    counts = Counter(
        item.get("billing_cycle", "Unknown")
        for item in active
    )

    print("\n--- Active Subscriptions by Billing Cycle ---")

    if not counts:
        print("No active subscriptions.")
        return

    for cycle, count in sorted(counts.items()):
        print(f"{cycle}: {count}")


def next_payment_forecast():
    subscriptions = load_subscriptions()

    active = [
        item for item in subscriptions
        if item.get("status") == "Active"
    ]

    active.sort(key=lambda item: item.get("next_payment", ""))

    print("\n--- Next Payment Forecast ---")

    if not active:
        print("No active subscriptions.")
        return

    for item in active:
        days = days_until(item["next_payment"])

        if days < 0:
            label = f"Overdue by {abs(days)} day(s)"
        elif days == 0:
            label = "Due today"
        else:
            label = f"{days} day(s) remaining"

        print(
            f"{item['subscription_id']} | "
            f"{item['name']} | "
            f"₹{item['amount']:.2f} | "
            f"{item['next_payment']} | {label}"
        )
