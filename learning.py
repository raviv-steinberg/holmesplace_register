from typing import Optional


def reverse_string(s: str) -> str:
    rev = list(s)
    for i in range(int(len(s) / 2)):
        rev[i], rev[len(rev) - i - 1] = rev[len(rev) - i - 1], rev[i]
    return ''.join(rev)


def reverse_list(l: list) -> list:
    for i in range(int(len(l) / 2)):
        l[i], l[len(l) - i - 1] = l[len(l) - i - 1], l[i]
    return l


def reverse_number(num: int):
    result = 0

    while num:
        remainder = num % 10
        result = (result * 10) + remainder
        num //= 10
    return result


def roman_to_int(roman: str) -> int:
    roman_values = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}

    result = 0
    prev_value = 0

    for char in reverse_string(roman):
        value = roman_values[char]
        if value < prev_value:
            result -= value
        else:
            result += value
        prev_value = value
    return result


def int_to_roman(number: int) -> str:
    val = [1, 4, 5, 9, 10, 40, 50, 90, 100, 400, 500, 900, 1000]
    sym = ['I', 'IV', 'V', 'IX', 'X', 'XL', 'L', 'XC', 'C', 'CD', 'D', 'CM', 'M']

    result = ''
    i = len(val) - 1

    while number > 0:
        for _ in range(number // val[i]):
            result += sym[i]
            number -= val[i]
        i -= 1
    return result


def find_pair(numbers: list, target: int) -> Optional[tuple[int, int]]:
    low, high = 0, len(numbers) - 1

    while low < high:
        if numbers[low] + numbers[high] == target:
            return numbers[low], numbers[high]
        if numbers[low] + numbers[high] < target:
            low += 1
        else:
            high -= 1
    return None


def find_pair_v2(numbers: list, target: int) -> Optional[tuple[int, int]]:
    dictionary = {}
    for i, e in enumerate(numbers):
        if target - e in dictionary:
            return e, numbers[dictionary.get(target - e)]
        dictionary[e] = i
    return None


def is_palindrome(s: str) -> bool:
    for i in range(int(len(s) / 2)):
        if s[i] != s[len(s) - i - 1]:
            return False
    return True


def is_palindrome_recursive(s: str) -> bool:
    if len(s) < 1:
        return True
    return s[0] == s[-1] and is_palindrome_recursive(s[1:-1])


def string_to_occurrences(s: str) -> str:
    dictionary = {}
    for c in s:
        dictionary[c] = dictionary.get(c, 0) + 1
    return ''.join(f'{k}{v}' for k, v in dictionary.items())


def occurrences_to_string(s: str) -> str:
    result = ''
    for i in range(0, len(s), 2):
        result += s[i] * int(s[i + 1])
    return result


def string_to_int(s: str) -> int:
    result = 0
    mul = 1
    length = len(s) - 1

    while length >= 0:
        result += int(s[length]) * mul
        mul *= 10
        length -= 1
    return result


def count_digits_recursive(num: int) -> int:
    if num < 10:
        return 1
    return count_digits_recursive(num=num // 10) + 1


def max_profit(numbers: list) -> int:
    profit = 0

    if numbers is None or len(numbers) == 0:
        return profit

    min_num = numbers[0]
    for num in numbers:
        if num < min_num:
            min_num = num
        else:
            if num - min_num > profit:
                profit = num - min_num
    return profit


def fibonacci(num: int) -> int:
    if num < 0:
        raise Exception('Invalid input')

    a = 0
    b = 1
    if num == 0:
        return a
    elif num == 1:
        return b

    for i in range(1, num):
        c = a + b
        a = b
        b = c
    return b


def fibonacci_recursive(num: int) -> int:
    if num < 0:
        raise Exception('Invalid input')
    elif num == 0:
        return 0
    elif num == 1 or num == 2:
        return 1
    return fibonacci_recursive(num - 1) + fibonacci_recursive(num - 2)


def add_one(l: list) -> list:
    length = len(l) - 1

    while length >= 0 and l[length] == 9:
        l[length] = 0
        length -= 1

    if length >= 0:
        l[length] += 1
    else:
        l.insert(0, 1)
    return l


# print(reverse_string('raviv'))
# print(reverse_list([1, 2, 3, 4, 5]))
# print(reverse_number(1234))
# print(roman_to_int('MMMDCCXXIV'))
# print(int_to_roman(3724))
# print(find_pair(numbers=[2, 3, 7, 2, 5], target=9))
# print(find_pair_v2(numbers=[2, 3, 7, 2, 5], target=9))
# print(is_palindrome('ravivar'))
# print(is_palindrome_recursive('ravivar'))
# print(string_to_occurrences('ccgerr'))
# print(occurrences_to_string('c2g1e1r2'))
# print(string_to_int('1234'))
# print(count_digits_recursive(1234))
# print(max_profit(numbers=[3, 1, 10, 16, 6]))
# print(fibonacci(2))
# print(fibonacci_recursive(2))
print(add_one([1, 2, 9]))
