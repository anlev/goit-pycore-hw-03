import random

def get_numbers_ticket(min_value: int, max_value: int, quantity: int) -> list[int]:
    if not isinstance(min_value, int) or not isinstance(max_value, int) or not isinstance(quantity, int):
        return []

    if min_value < 1 or max_value > 1000 or min_value > max_value:
        return []

    pool_size = max_value - min_value + 1
    if quantity < 1 or quantity > pool_size:
        return []

    numbers = random.sample(range(min_value, max_value + 1), k=quantity)
    return sorted(numbers)

print(get_numbers_ticket(1, 49, 6))

# Tests
nums = get_numbers_ticket(1, 49, 6)
assert len(nums) == 6
assert nums == sorted(nums)
assert len(set(nums)) == 6

assert get_numbers_ticket(7, 7, 1) == [7]   # single-value range

assert get_numbers_ticket(1, 10, 0) == []   # quantity too small
assert get_numbers_ticket(5, 4, 2) == []    # min > max
assert get_numbers_ticket(0, 10, 3) == []   # min < 1