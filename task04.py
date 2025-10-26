from datetime import datetime, date, timedelta
import calendar

def clamp_to_month_end(year: int, month: int, day: int) -> date:
    last_day = calendar.monthrange(year, month)[1]
    return date(year, month, min(day, last_day))

def parse_birthday(s: str) -> date:
    try:
        return datetime.strptime(s, "%Y.%m.%d").date()
    except ValueError:
        year, month, day = map(int, s.split("."))
        if not (1 <= month <= 12):
            raise ValueError("Invalid month")
        if year <= 0:
            raise ValueError("Invalid year")
        return clamp_to_month_end(year, month, day)
    except Exception as e:
        raise ValueError(f"Invalid birthday: {s}") from e


def next_monday(d: date) -> date:
    wd = d.weekday()  # 0=Mon ... 6=Sun
    if wd == 5:
        return d + timedelta(days=2)
    if wd == 6:
        return d + timedelta(days=1)
    return d


def get_upcoming_birthdays(users, today = date.today()):
    result = []
    for user in users:
        birthday = parse_birthday(user["birthday"])
        birthday_this_year = clamp_to_month_end(year = today.year, month = birthday.month, day = birthday.day)
        next_birthday = birthday_this_year if birthday_this_year >= birthday else clamp_to_month_end(year = today.year + 1, month = birthday.month, day = birthday.day)

        days_remaining = (next_birthday - today).days

        if 0 <= days_remaining < 7:
            congratulation_date = next_monday(next_birthday)
            result.append({
                "name": user["name"],
                "congratulation_date": congratulation_date.strftime("%Y.%m.%d")
            })

    result.sort(key = lambda x: (x["congratulation_date"], x["name"]))
    return result

# Tests
today = date(2024, 1, 22)
users = [
    {"name": "John Doe",        "birthday": "1985.01.23"},
    {"name": "Jane Smith",      "birthday": "1990.01.27"},
    {"name": "Past this year",  "birthday": "1988.01.10"},
    {"name": "Today",           "birthday": "1991.01.22"},
    {"name": "Exactly 7 days",  "birthday": "1970.01.29"},
]
expected = [
    {"name": "Today",            "congratulation_date": "2024.01.22"},
    {"name": "John Doe",         "congratulation_date": "2024.01.23"},
    {"name": "Exactly 7 days",   "congratulation_date": "2024.01.29"},
    {"name": "Jane Smith",       "congratulation_date": "2024.01.29"},
]
got = get_upcoming_birthdays(users, today=today)
print(got)
print(expected)
assert got == expected, f"TEST 1 failed:\nExpected: {expected}\nGot: {got}"

today = date(2025, 2, 24)
users = [{"name": "Leap Year", "birthday": "2000.02.29"}]
expected = [{"name": "Leap Year", "congratulation_date": "2025.02.28"}]
got = get_upcoming_birthdays(users, today=today)
assert got == expected, f"TEST 2 failed:\nExpected: {expected}\nGot: {got}"

today = date(2024, 2, 26)  # Пн перед 29.02.2024 (високосний)
users = [{"name": "Leap Year OK", "birthday": "2016.02.29"}]
expected = [{"name": "Leap Year OK", "congratulation_date": "2024.02.29"}]
got = get_upcoming_birthdays(users, today=today)
assert got == expected, f"TEST 3 failed:\nExpected: {expected}\nGot: {got}"

today = date(2024, 4, 24)
users = [{"name": "April Leap", "birthday": "1990.04.31"}]
expected = [{"name": "April Leap", "congratulation_date": "2024.04.30"}]
got = get_upcoming_birthdays(users, today=today)
assert got == expected, f"TEST 4 failed:\nExpected: {expected}\nGot: {got}"

today = date(2024, 3, 5)
users = [
    {"name": "Exactly today",  "birthday": "2000.03.05"},
    {"name": "In seven days",  "birthday": "2000.03.12"},
    {"name": "Too far",        "birthday": "2000.03.13"},
]
expected = [
    {"name": "Exactly today", "congratulation_date": "2024.03.05"},
    {"name": "In seven days", "congratulation_date": "2024.03.12"},
]
got = get_upcoming_birthdays(users, today=today)
assert got == expected, f"TEST 5 failed:\nExpected: {expected}\nGot: {got}"
