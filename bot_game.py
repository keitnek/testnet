import random
import csv
import os
import time
import pyautogui

# TỰ ĐỘNG NHẬN DIỆN THƯ MỤC HIỆN TẠI (Dùng cho GitHub/Máy khác cực tiện)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "data_bot.csv")
ACCOUNT_FILE = os.path.join(BASE_DIR, "account.csv")

def khoi_tao():
    """Khởi tạo file tài khoản nếu chưa có"""
    if not os.path.exists(ACCOUNT_FILE) or os.path.getsize(ACCOUNT_FILE) == 0:
        with open(ACCOUNT_FILE, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["Số dư"])
            writer.writerow([1000000]) # Tặng 1 triệu khởi nghiệp
        print("💰 Đã khởi tạo ví tiền mới: 1,000,000 VNĐ")

def choi_game():
    khoi_tao()
    
    # 1. Đọc số dư
    with open(ACCOUNT_FILE, mode='r', encoding='utf-8') as f:
        rows = list(csv.reader(f))
        balance = int(rows[1][0])

    print(f"\n" + "="*30)
    print(f"💳 SỐ DƯ HIỆN TẠI: {balance:,} VNĐ")
    print("="*30)
    
    # 2. Nhập lệnh cược
    try:
        bet = int(input("💰 Nhập tiền cược: "))
        if bet > balance:
            print("⚠️ Bạn không đủ tiền!")
            return
        if bet <= 0:
            print("❌ Tiền cược phải lớn hơn 0!")
            return
        
        print("\n--- CHỌN CỬA ĐẶT ---")
        print("1. Tài (0-4) | 2. Xỉu (5-9)")
        print("3. Chẵn      | 4. Lẻ")
        choice_input = input("👉 Lựa chọn của bạn (1/2/3/4): ")
        if choice_input not in ['1', '2', '3', '4']:
            print("❌ Lựa chọn không hợp lệ!")
            return
    except ValueError:
        print("❌ Vui lòng chỉ nhập số!")
        return

    # 3. KÍCH HOẠT QUAY SỐ (Bắt đầu sau khi nhận lệnh cược)
    so_moi = str(random.randint(1, 99)).zfill(2)
    
    # Ghi đè vào file dữ liệu
    with open(DATA_FILE, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Gia_Tri"])
        writer.writerow([so_moi])

    # 4. GÕ VÀO EMU8086 (Độ trễ 100ms)
    print("\n⌨️ Đang chuẩn bị nhập liệu...")
    print("⚡ HÃY CHUYỂN SANG CỬA SỔ EMU8086 NGAY (3 giây)...")
    time.sleep(3)
    
    # Gõ số vào emu8086 với độ trễ 0.1s (100ms)
    pyautogui.typewrite(so_moi, interval=0.1)
    pyautogui.press('enter')

    # 5. XỬ LÝ KẾT QUẢ (a + b)
    a, b = int(so_moi[0]), int(so_moi[1])
    d = (a + b) % 10
    
    is_tai = 0 <= d <= 4
    is_chan = d in [0, 2, 4, 6, 8]
    
    win = False
    if choice_input == '1' and is_tai: win = True
    elif choice_input == '2' and not is_tai: win = True
    elif choice_input == '3' and is_chan: win = True
    elif choice_input == '4' and not is_chan: win = True

    # 6. HIỂN THỊ KẾT QUẢ
    ten_so = "TÀI" if is_tai else "XỈU"
    ten_cl = "CHẴN" if is_chan else "LẺ"
    
    print(f"\n🎯 KẾT QUẢ HỆ THỐNG:")
    print(f"   🔹 Con số: {so_moi} ({a} + {b} = {a+b})")
    print(f"   🔹 Đơn vị: {d} -> [{ten_so}] và [{ten_cl}]")

    if win:
        balance += bet
        print(f"✅ THẮNG LỚN! +{bet:,} VNĐ")
    else:
        balance -= bet
        print(f"❌ THUA RỒI! -{bet:,} VNĐ")

    # 7. CẬP NHẬT VÍ TIỀN
    with open(ACCOUNT_FILE, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Số dư"])
        writer.writerow([balance])
    
    print(f"💳 Số dư mới: {balance:,} VNĐ")

if __name__ == "__main__":
    while True:
        chay_game()
        print("\n" + "-"*30)
        tiep = input("Bạn có muốn chơi tiếp ván mới? (c/k): ")
        if tiep.lower() != 'c':
            print("Cảm ơn bạn đã chơi! Tạm biệt.")
            break
