import os
import random
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from shared.student import STUDENT_NAME, VARIANT_NUMBER

PASSWORDS = [
    "password123",
    "Qwerty!2023",
    "admin",
    "MyP@ssword",
    "123456",
    "SecurePass!",
    "test",
    "P@ssword123",
    "welcome",
    "StrongP@ss1",
]

CRITERIA = {
    "min_length": 8,
    "require_digits": True,
    "require_upper": True,
    "require_special": True,
}

FORBIDDEN_PASSWORDS = {
    "password",
    "123456",
    "admin",
    "test",
    "welcome",
    "qwerty",
}


def add_random_duplicates(passwords_list):
    result = list(passwords_list)
    for _ in range(3):
        idx = random.randint(0, len(passwords_list) - 1)
        result.append(passwords_list[idx])
    return result


def check_strength(password, all_passwords, criteria, forbidden):
    min_len = criteria["min_length"]

    if password.lower() in forbidden or len(password) < min_len:
        return "Заборонений"

    has_digit = any(c.isdigit() for c in password)
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_special = any(not c.isalnum() for c in password)

    all_criteria = has_digit and has_upper and has_lower and has_special
    is_unique = all_passwords.count(password) == 1

    if all_criteria and len(password) >= (min_len + 4) and is_unique:
        return "Дуже сильний"

    if all_criteria and len(password) < (min_len + 4):
        return "Сильний"

    matched = sum([has_digit, has_upper, has_lower, has_special])
    if len(password) >= min_len and matched > 1:
        return "Середній"

    if matched >= 1:
        return "Слабкий"

    return "Заборонений"


def run_task1():
    print("=" * 60)
    print(f"Завдання 1 | Студент: {STUDENT_NAME} | Варіант: {VARIANT_NUMBER}")
    print("=" * 60)

    work_passwords = add_random_duplicates(PASSWORDS)

    print(f"{'№':<4} {'Пароль':<16} {'Довжина':<10} {'Надійність'}")
    print("-" * 55)

    for i, pwd in enumerate(work_passwords, 1):
        grade = check_strength(pwd, work_passwords, CRITERIA, FORBIDDEN_PASSWORDS)
        print(f"{i:<4} {pwd:<16} {len(pwd):<10} {grade}")


if __name__ == "__main__":
    run_task1()
