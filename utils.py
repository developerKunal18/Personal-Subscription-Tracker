import calendar
from datetime import date, datetime, timedelta

from config import DATE_FORMAT, BILLING_CYCLES


def get_text(prompt):
    while True:
        value = input(prompt).strip()

        if value:
            return value

        print("This field cannot be empty.")


def get_amount(prompt):
    while True:
        try:
            amount = float(input(prompt).strip())

            if amount < 0:
                print("Amount cannot be negative.")
                continue

            return round(amount, 2)

        except ValueError:
            print("Enter a valid amount.")


def get_date(prompt):
    while True:
        value = input(prompt).strip()

        try:
            parsed = datetime.strptime(value, DATE_FORMAT).date()

            if parsed.strftime(DATE_FORMAT) != value:
                raise ValueError

            return value

        except ValueError:
            print("Enter a valid date in YYYY-MM-DD format.")


def get_optional_date(prompt, current_value):
    value = input(f"{prompt} [{current_value}]: ").strip()

    if not value:
        return current_value

    try:
        parsed = datetime.strptime(value, DATE_FORMAT).date()

        if parsed.strftime(DATE_FORMAT) != value:
            raise ValueError

        return value

    except ValueError:
        print("Invalid date. Keeping the previous date.")
        return current_value


def get_choice(prompt, options):
    print("\nAvailable options:")

    for index, option in enumerate(options, start=1):
        print(f"{index}. {option}")

    while True:
        value = input(prompt).strip()

        if value.isdigit():
            number = int(value)

            if 1 <= number <= len(options):
                return options[number - 1]

        print(f"Choose a number between 1 and {len(options)}.")


def get_optional_choice(prompt, current_value, options):
    answer = input(
        f"Change {prompt}? Current: {current_value} (y/n): "
    ).strip().lower()

    if answer == "y":
        return get_choice(f"Select {prompt}: ", options)

    return current_value


def next_billing_date(start_date, cycle):
    current = datetime.strptime(start_date, DATE_FORMAT).date()

    if cycle == "Weekly":
        result = current + timedelta(days=7)

    elif cycle in ("Monthly", "Quarterly", "Half-Yearly", "Yearly"):
        months = {
            "Monthly": 1,
            "Quarterly": 3,
            "Half-Yearly": 6,
            "Yearly": 12
        }[cycle]

        month_index = current.month - 1 + months
        year = current.year + month_index // 12
        month = month_index % 12 + 1

        day = min(current.day, calendar.monthrange(year, month)[1])
        result = date(year, month, day)

    else:
        raise ValueError("Unsupported billing cycle.")

    return result.strftime(DATE_FORMAT)


def days_until(date_string):
    target = datetime.strptime(date_string, DATE_FORMAT).date()
    return (target - date.today()).days


def current_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def pause():
    input("\nPress Enter to continue...")
