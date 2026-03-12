import csv
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "data_bot.csv")
HISTORY_FILE = os.path.join(BASE_DIR, "history.csv")

def save_current_round(number):
    with open(DATA_FILE, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Gia_Tri"])
        writer.writerow([number])

def log_history(round_num, num, bet, choice, result, balance):
    file_exists = os.path.isfile(HISTORY_FILE)
    with open(HISTORY_FILE, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Lượt", "Số", "Cược", "Cửa", "Kết quả", "Số dư"])
        writer.writerow([round_num, num, bet, choice, result, balance])
