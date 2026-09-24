import os
import sys

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
)
from shared.student import STUDENT_NAME, VARIANT_NUMBER

USERS = {
    "admin001": {
        "role": "administrator",
        "clearance": 4,
        "department": "IT",
        "active": True,
    },
    "user123": {
        "role": "analyst",
        "clearance": 2,
        "department": "Security",
        "active": True,
    },
    "guest789": {
        "role": "guest",
        "clearance": 1,
        "department": "External",
        "active": True,
    },
    "manager456": {
        "role": "manager",
        "clearance": 3,
        "department": "Operations",
        "active": True,
    },
    "contractor99": {
        "role": "contractor",
        "clearance": 1,
        "department": "External",
        "active": False,
    },
}

RESOURCES = [
    ("database_backup", 4),
    ("user_logs", 2),
    ("public_docs", 1),
    ("financial_reports", 3),
    ("system_config", 4),
    ("training_materials", 1),
    ("security_policies", 3),
    ("audit_logs", 4),
    ("employee_data", 3),
    ("temp_files", 1),
]

SECURITY_LEVELS = ("Public", "Internal", "Confidential", "Secret")
BLOCKED_USERS = {"contractor99", "temp_user", "suspended_acc"}


def show_resources():
    print("\nСписок ресурсів системи:")
    print(f"{'№':<4} {'Ресурс':<24} {'Рівень безпеки'}")
    print("-" * 50)
    for i, (name, lvl) in enumerate(RESOURCES, 1):
        lvl_name = SECURITY_LEVELS[lvl - 1]
        print(f"{i:<4} {name:<24} {lvl_name}")


def check_user_access(username, resource):
    _, req_clearance = resource

    if username not in USERS:
        return "DENY (User not found)"

    if username in BLOCKED_USERS:
        return "DENY (User is blocked)"

    user = USERS[username]
    if not user.get("active"):
        return "DENY (Account inactive)"

    if user.get("clearance", 0) >= req_clearance:
        return "ALLOW"

    return "DENY (Insufficient clearance)"


def run_task2():
    print("=" * 60)
    print(f"Завдання 2 | Студент: {STUDENT_NAME} | Варіант: {VARIANT_NUMBER}")
    print("=" * 60)

    show_resources()

    print("\nРезультати перевірки доступу:")
    users_to_test = list(USERS.keys()) + ["guest_unknown"]

    for user in users_to_test:
        for res in RESOURCES:
            status = check_user_access(user, res)
            print(f"user=[{user}] resource=[{res[0]}] -> {status}")


if __name__ == "__main__":
    run_task2()