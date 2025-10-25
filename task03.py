import re

def normalize_phone(phone_number: str) -> str:
    if phone_number is None:
        return ""

    s = str(phone_number).strip()
    digits = re.sub(r"\D", "", s)
    if not digits:
        return ""

    has_international_code = s.startswith("+") or digits.startswith("38")

    if has_international_code:
        return "+" + digits

    return "+38" + digits

# Tests
raw_numbers = [
    "067\\t123 4567",
    "(095) 234-5678\\n",
    "+380 44 123 4567",
    "380501234567",
    "    +38(050)123-32-34",
    "     0503451234",
    "(050)8889900",
    "38050-111-22-22",
    "38050 111 22 11   ",
]

expected_numbers = [
    '+380671234567',
    '+380952345678',
    '+380441234567',
    '+380501234567',
    '+380501233234',
    '+380503451234',
    '+380508889900',
    '+380501112222',
    '+380501112211',
]
normalized_numbers = [normalize_phone(n) for n in raw_numbers]
assert normalized_numbers == expected_numbers, f"Expected {expected_numbers}, got {normalized_numbers}"

assert normalize_phone(None) == ""
assert normalize_phone("") == ""
assert normalize_phone("   ") == ""

assert normalize_phone("+380501234567") == "+380501234567"
assert normalize_phone("+380 (50) 123-45-67") == "+380501234567"

assert normalize_phone("050 123 45 67") == "+380501234567"
assert normalize_phone("067-123-45-67") == "+380671234567"

assert normalize_phone("380501234567") == "+380501234567"
assert normalize_phone("38 050 123 45 67") == "+380501234567"

assert normalize_phone("+1 (202) 555-0175") == "+12025550175"