# Personal Subscription Tracker

A simple Python application to manage recurring subscriptions, monitor upcoming payments, and estimate monthly and yearly subscription expenses.

## Features

- Add, view, search, edit, and delete subscriptions
- Track subscription providers and costs
- Support weekly, monthly, quarterly, half-yearly, and yearly billing
- Record the next payment date
- Track active and cancelled subscriptions
- View upcoming payments and overdue subscriptions
- Record payments and advance the next billing date
- Calculate estimated monthly and yearly expenses
- Generate provider-wise and billing-cycle reports
- Store data in JSON format

## Technologies Used

- Python 3
- JSON
- datetime
- calendar
- collections

## Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/Personal-Subscription-Tracker.git
```

Open the project directory:

```bash
cd Personal-Subscription-Tracker
```

Run the application:

```bash
python main.py
```

No external packages are required.

## Project Structure

```text
Personal-Subscription-Tracker/
├── main.py
├── config.py
├── storage.py
├── utils.py
├── subscription_manager.py
├── report_manager.py
├── requirements.txt
├── .gitignore
├── README.md
└── data/
    └── subscriptions.json
```

## How to Use

1. Add a subscription and enter its cost and billing cycle.
2. Enter the next payment date.
3. Review upcoming or overdue payments.
4. Record a payment to advance the next billing date.
5. Review monthly and yearly spending estimates.
6. Edit or cancel subscriptions when needed.

## Learning Outcomes

- Python modules and functions
- JSON file handling
- Date and calendar calculations
- Lists, dictionaries, and counters
- Searching and filtering
- Financial calculations
- Menu-driven application development

## Future Improvements

- Add a graphical user interface
- Integrate SQLite or MySQL
- Export reports to CSV
- Add email or desktop reminders
- Maintain a complete payment history
- Add budget limits and spending charts

## Author

Python Project Challenge 

## License

Free to use for educational and personal learning purposes.
