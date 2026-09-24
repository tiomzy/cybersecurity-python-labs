import csv
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from functools import wraps

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
)
from shared.student import STUDENT_NAME, VARIANT_NUMBER

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
CSV_PATH = os.path.join(DATA_DIR, "users.csv")
LOG_PATH = os.path.join(DATA_DIR, "log.json")

MIN_LEN = 12
SALT = str(VARIANT_NUMBER).zfill(5)


class ValidationError(Exception):
    pass


def log_event(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        username = args[0] if len(args) > 0 else kwargs.get("username", "")
        success = False
        try:
            success = func(*args, **kwargs)
            return success
        finally:
            entry = {
                "event": "login",
                "user": username,
                "result": "success" if success else "failure",
                "timestamp": datetime.now(timezone.utc).strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                "args": list(args),
                "kwargs": kwargs,
            }
            os.makedirs(DATA_DIR, exist_ok=True)
            logs = []
            if os.path.exists(LOG_PATH):
                try:
                    with open(LOG_PATH, "r", encoding="utf-8") as f:
                        logs = json.load(f)
                except (json.JSONDecodeError, OSError):
                    logs = []

            logs.append(entry)
            with open(LOG_PATH, "w", encoding="utf-8") as f:
                json.dump(logs, f, indent=4, ensure_ascii=False)

    return wrapper


def generate_hash(password: str, salt: str = "00000") -> str:
    if not password or not salt:
        raise ValueError("Пароль або сіль порожні")

    if len(password) < MIN_LEN:
        raise ValidationError(f"Пароль менший за {MIN_LEN} символів")

    data = (password + salt).encode("utf-8")
    return hashlib.sha3_512(data).hexdigest()


def create_user(username, password):
    h = generate_hash(password, SALT)
    return username, h


def create_users(users_list):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["username", "password_hash"])
        for login_name, pwd in users_list:
            u, h = create_user(login_name, pwd)
            writer.writerow([u, h])


def read_users_db():
    if not os.path.exists(CSV_PATH):
        raise FileNotFoundError(f"Файл {CSV_PATH} не знайдено")

    with open(CSV_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)


@log_event
def login(username: str, password: str, users_db: list) -> bool:
    if not username or not password:
        raise ValueError("Логін та пароль мають бути заповнені")

    for row in users_db:
        if row["username"] == username:
            try:
                curr_hash = generate_hash(password, SALT)
            except ValidationError:
                return False
            return curr_hash == row["password_hash"]

    return False


def run_task3():
    print("=" * 60)
    print(f"Завдання 3 | Студент: {STUDENT_NAME} | Варіант: {VARIANT_NUMBER}")
    print("=" * 60)

    users_to_register = (
        ("alpha_user", "Secur3Passw0rd!"),
        ("beta_tester", "MySecretP@ss2026"),
        ("charlie_dev", "C0dingInPythonNow!"),
        ("delta_admin", "Sup3rRootP@ssword"),
        ("echo_analyst", "An@lysisD@ta1234"),
        ("foxtrot_ops", "0p3rations2026##"),
        ("golf_lead", "M@nag3mentL3ad99"),
        ("hotel_guest", "G@estV1sit0r2026"),
        ("india_audit", "Aud1tCh3ckP@ss!"),
        ("juliet_sec", "S3curityD3f3ns3!"),
    )

    try:
        create_users(users_to_register)
        print("Базу users.csv успішно створено.")

        db = read_users_db()
        print("\nСписок користувачів із бази даних:")
        print(f"{'№':<3} {'Логін':<16} {'Хеш (перші 25 симв.)'}")
        print("-" * 50)
        for i, row in enumerate(db, 1):
            print(f"{i:<3} {row['username']:<16} {row['password_hash'][:25]}...")

        print("\nПеревірка авторизації:")
        test_data = [
            ("alpha_user", "Secur3Passw0rd!"),
            ("delta_admin", "BadPassword123"),
            ("hotel_guest", "G@estV1sit0r2026"),
            ("ghost_user", "SomeSecret12345!"),
        ]

        for u, p in test_data:
            res = login(u, p, db)
            print(f"Вхід [{u}] -> {'Успішно' if res else 'Невдало'}")

        print("\nЖурнал log.json оновлено.")

    except (OSError, FileNotFoundError, PermissionError) as fe:
        print(f"Помилка файлу: {fe}")
    except (ValidationError, ValueError) as ve:
        print(f"Помилка валідації: {ve}")


if __name__ == "__main__":
    run_task3()