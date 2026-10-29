from storage import initialize_storage

from subscription_manager import (
    add_subscription,
    view_subscriptions,
    search_subscriptions,
    edit_subscription,
    delete_subscription,
    record_payment,
    view_upcoming_payments,
    view_overdue_payments
)

from report_manager import (
    spending_report,
    provider_report,
    billing_cycle_report,
    next_payment_forecast
)

from utils import pause


def show_menu():
    print("\n" + "=" * 46)
    print("        PERSONAL SUBSCRIPTION TRACKER")
    print("=" * 46)
    print("1. Add Subscription")
    print("2. View All Subscriptions")
    print("3. Search Subscriptions")
    print("4. Edit Subscription")
    print("5. Delete Subscription")
    print("6. Record Payment")
    print("7. Payments Due Within 7 Days")
    print("8. Overdue Payments")
    print("9. Spending Report")
    print("10. Provider-Wise Report")
    print("11. Billing Cycle Report")
    print("12. Next Payment Forecast")
    print("0. Exit")
    print("=" * 46)


def main():
    initialize_storage()

    actions = {
        "1": add_subscription,
        "2": view_subscriptions,
        "3": search_subscriptions,
        "4": edit_subscription,
        "5": delete_subscription,
        "6": record_payment,
        "7": view_upcoming_payments,
        "8": view_overdue_payments,
        "9": spending_report,
        "10": provider_report,
        "11": billing_cycle_report,
        "12": next_payment_forecast
    }

    while True:
        show_menu()
        choice = input("Enter your choice: ").strip()

        if choice == "0":
            print("Thank you for using Personal Subscription Tracker!")
            break

        action = actions.get(choice)

        if action:
            try:
                action()
            except (OSError, ValueError, KeyError, TypeError) as error:
                print(f"An error occurred: {error}")

            pause()
        else:
            print("Invalid choice. Select a number from 0 to 12.")
            pause()


if __name__ == "__main__":
    main()
