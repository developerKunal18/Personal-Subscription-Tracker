from datetime import datetime

from config import BILLING_CYCLES, SUBSCRIPTION_STATUSES, DATE_FORMAT
from storage import load_subscriptions, save_subscriptions
from utils import (
    get_text,
    get_amount,
    get_date,
    get_choice,
    get_optional_date,
    get_optional_choice,
    days_until,
    current_timestamp,
    next_billing_date
)


def generate_subscription_id(subscriptions):
    highest = 0

    for subscription in subscriptions:
        subscription_id = subscription.get("subscription_id", "")

        if subscription_id.startswith("SUB"):
            try:
                highest = max(highest, int(subscription_id[3:]))
            except ValueError:
                continue

    return f"SUB{highest + 1:04d}"


def add_subscription():
    subscriptions = load_subscriptions()

    print("\n--- Add Subscription ---")

    name = get_text("Subscription name: ")
    provider = get_text("Provider/company: ")
    amount = get_amount("Subscription cost (₹): ")
    cycle = get_choice("Billing cycle: ", BILLING_CYCLES)
    next_payment = get_date("Next payment date (YYYY-MM-DD): ")
    notes = input("Notes (optional): ").strip()

    subscription = {
        "subscription_id": generate_subscription_id(subscriptions),
        "name": name,
        "provider": provider,
        "amount": amount,
        "billing_cycle": cycle,
        "next_payment": next_payment,
        "status": "Active",
        "notes": notes,
        "created_at": current_timestamp(),
        "updated_at": current_timestamp()
    }

    subscriptions.append(subscription)
    save_subscriptions(subscriptions)

    print("\nSubscription added successfully.")
    print(f"Subscription ID: {subscription['subscription_id']}")
    print(f"Next payment: {next_payment}")


def display_subscription(subscription):
    payment_date = subscription["next_payment"]
    remaining = days_until(payment_date)

    if subscription["status"] == "Cancelled":
        payment_message = "Cancelled"
    elif remaining < 0:
        payment_message = f"Overdue by {abs(remaining)} day(s)"
    elif remaining == 0:
        payment_message = "Payment due today"
    else:
        payment_message = f"{remaining} day(s) remaining"

    print("-" * 48)
    print(f"ID             : {subscription['subscription_id']}")
    print(f"Name           : {subscription['name']}")
    print(f"Provider       : {subscription['provider']}")
    print(f"Cost           : ₹{subscription['amount']:.2f}")
    print(f"Billing Cycle  : {subscription['billing_cycle']}")
    print(f"Next Payment   : {payment_date}")
    print(f"Payment Alert  : {payment_message}")
    print(f"Status         : {subscription['status']}")
    print(f"Notes          : {subscription.get('notes', '')}")
    print("-" * 48)


def view_subscriptions():
    subscriptions = load_subscriptions()

    print("\n--- All Subscriptions ---")

    if not subscriptions:
        print("No subscriptions found.")
        return

    for subscription in sorted(
        subscriptions,
        key=lambda item: item.get("next_payment", "")
    ):
        display_subscription(subscription)

    print(f"Total subscriptions: {len(subscriptions)}")


def search_subscriptions():
    subscriptions = load_subscriptions()

    keyword = input(
        "Search by ID, subscription name, or provider: "
    ).strip().lower()

    if not keyword:
        print("Enter a search term.")
        return

    results = [
        item for item in subscriptions
        if keyword in item.get("subscription_id", "").lower()
        or keyword in item.get("name", "").lower()
        or keyword in item.get("provider", "").lower()
    ]

    if not results:
        print("No matching subscriptions found.")
        return

    for subscription in results:
        display_subscription(subscription)


def find_subscription(subscriptions, subscription_id):
    for subscription in subscriptions:
        if subscription.get("subscription_id", "").upper() == subscription_id:
            return subscription

    return None


def edit_subscription():
    subscriptions = load_subscriptions()
    subscription_id = input(
        "Enter subscription ID to edit: "
    ).strip().upper()

    subscription = find_subscription(subscriptions, subscription_id)

    if not subscription:
        print("Subscription not found.")
        return

    print("Leave text fields blank to keep their current values.")

    name = input(f"Name [{subscription['name']}]: ").strip()
    provider = input(f"Provider [{subscription['provider']}]: ").strip()
    notes = input(f"Notes [{subscription.get('notes', '')}]: ").strip()

    if name:
        subscription["name"] = name

    if provider:
        subscription["provider"] = provider

    if notes:
        subscription["notes"] = notes

    change_amount = input(
        f"Change amount? Current ₹{subscription['amount']:.2f} (y/n): "
    ).strip().lower()

    if change_amount == "y":
        subscription["amount"] = get_amount("New amount (₹): ")

    subscription["billing_cycle"] = get_optional_choice(
        "billing cycle",
        subscription["billing_cycle"],
        BILLING_CYCLES
    )

    subscription["next_payment"] = get_optional_date(
        "Next payment date",
        subscription["next_payment"]
    )

    subscription["status"] = get_optional_choice(
        "status",
        subscription["status"],
        SUBSCRIPTION_STATUSES
    )

    try:
        datetime.strptime(subscription["next_payment"], DATE_FORMAT)
    except ValueError:
        print("Invalid date. Changes were not saved.")
        return

    subscription["updated_at"] = current_timestamp()
    save_subscriptions(subscriptions)

    print("Subscription updated successfully.")


def delete_subscription():
    subscriptions = load_subscriptions()
    subscription_id = input(
        "Enter subscription ID to delete: "
    ).strip().upper()

    subscription = find_subscription(subscriptions, subscription_id)

    if not subscription:
        print("Subscription not found.")
        return

    display_subscription(subscription)

    confirm = input("Delete this subscription? (y/n): ").strip().lower()

    if confirm == "y":
        subscriptions.remove(subscription)
        save_subscriptions(subscriptions)
        print("Subscription deleted successfully.")
    else:
        print("Deletion cancelled.")


def record_payment():
    subscriptions = load_subscriptions()
    subscription_id = input(
        "Enter subscription ID paid: "
    ).strip().upper()

    subscription = find_subscription(subscriptions, subscription_id)

    if not subscription:
        print("Subscription not found.")
        return

    if subscription["status"] == "Cancelled":
        print("This subscription is cancelled.")
        return

    old_date = subscription["next_payment"]
    subscription["next_payment"] = next_billing_date(
        old_date,
        subscription["billing_cycle"]
    )
    subscription["updated_at"] = current_timestamp()

    save_subscriptions(subscriptions)

    print("Payment recorded and next payment date updated.")
    print(f"Previous due date: {old_date}")
    print(f"Next payment date: {subscription['next_payment']}")


def view_upcoming_payments():
    subscriptions = load_subscriptions()

    upcoming = [
        item for item in subscriptions
        if item["status"] == "Active"
        and 0 <= days_until(item["next_payment"]) <= 7
    ]

    upcoming.sort(key=lambda item: item["next_payment"])

    print("\n--- Payments Due Within 7 Days ---")

    if not upcoming:
        print("No payments due within the next 7 days.")
        return

    for subscription in upcoming:
        display_subscription(subscription)


def view_overdue_payments():
    subscriptions = load_subscriptions()

    overdue = [
        item for item in subscriptions
        if item["status"] == "Active"
        and days_until(item["next_payment"]) < 0
    ]

    overdue.sort(key=lambda item: item["next_payment"])

    print("\n--- Overdue Subscription Payments ---")

    if not overdue:
        print("No overdue payments.")
        return

    for subscription in overdue:
        display_subscription(subscription)
