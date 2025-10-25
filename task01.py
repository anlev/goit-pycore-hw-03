from datetime import datetime, timedelta

def get_days_from_today(date: str) -> int:
    if not isinstance(date, str):
        raise ValueError("Date must be a string in 'YYYY-MM-DD' format")

    try:
        input_date = datetime.strptime(date.strip(), "%Y-%m-%d").date()

    except ValueError as e:
        raise ValueError("Date must be a string in 'YYYY-MM-DD' format") from e

    today_date = datetime.today().date()
    return (today_date - input_date).days


# Tests
def format_date(date) -> str:
    return date.strftime("%Y-%m-%d")

today = datetime.today().date()
yesterday = today - timedelta(days=1)
tomorrow = today + timedelta(days=1)

assert get_days_from_today(format_date(today)) == 0
assert get_days_from_today(format_date(yesterday)) == 1
assert get_days_from_today(format_date(tomorrow)) == -1

def expect_value_error(date):
    try:
        get_days_from_today(date)
    except ValueError:
        return
    raise AssertionError("Expected ValueError was not raised")

expect_value_error("2021/10/09")
expect_value_error("2021-02-30")
expect_value_error(20211009)