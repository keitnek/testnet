import csv
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ACCOUNT_FILE = os.path.join(BASE_DIR, "account.csv")

def get_balance():
    if not os.path.exists(ACCOUNT_FILE) or os.path.getsize(ACCOUNT_FILE) == 0:
        update_balance(1000000)
        return 1000000
    with open(ACCOUNT_FILE, mode='r', encoding='utf-8') as f:
        return int(list(csv.reader(f))[1][0])

def update_balance(new_amount):
    with open(ACCOUNT_FILE, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Số dư"])
        writer.writerow([new_amount])
