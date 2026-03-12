import time
import pyautogui
import generator
import wallet
import storage

def play_game():
    balance = wallet.get_balance()
    print(f"\n💰 Ví tiền: {balance:,} VNĐ")

    try:
        bet = int(input("💵 Nhập tiền cược: "))
        if bet > balance or bet <= 0:
            print("❌ Tiền không đủ hoặc không hợp lệ!"); return
        
        print("1. Tài (0-4) | 2. Xỉu (5-9) | 3. Chẵn | 4. Lẻ")
        choice_idx = input("👉 Chọn cửa (1-4): ")
        mapping = {"1": "Tài", "2": "Xỉu", "3": "Chẵn", "4": "Lẻ"}
        if choice_idx not in mapping: print("❌ Chọn sai!"); return
    except ValueError: print("❌ Chỉ nhập số!"); return

    # --- KÍCH HOẠT HỆ THỐNG ---
    secret_num = generator.generate_number() # 1. Random
    storage.save_current_round(secret_num)   # 2. Lưu số

    print("⚡ CHUYỂN SANG EMU8086 TRONG 3 GIÂY...")
    time.sleep(3)
    pyautogui.typewrite(secret_num, interval=0.1) # 3. Gõ phím (trễ 100ms)
    pyautogui.press('enter')

    # 4. Xử lý logic thắng thua
    a, b = int(secret_num[0]), int(secret_num[1])
    d = (a + b) % 10
    
    is_tai = 0 <= d <= 4
    is_chan = d in [0, 2, 4, 6, 8]
    
    win = False
    if choice_idx == '1' and is_tai: win = True
    elif choice_idx == '2' and not is_tai: win = True
    elif choice_idx == '3' and is_chan: win = True
    elif choice_idx == '4' and not is_chan: win = True

    # 5. Cập nhật ví và lịch sử
    balance = balance + bet if win else balance - bet
    wallet.update_balance(balance)
    res_text = "THẮNG" if win else "THUA"
    storage.log_history("Auto", secret_num, bet, mapping[choice_idx], res_text, balance)

    print(f"🎯 Kết quả: {secret_num} -> Đơn vị: {d} ({'Tài' if is_tai else 'Xỉu'} - {'Chẵn' if is_chan else 'Lẻ'})")
    print(f"📢 Bạn {res_text}! Số dư mới: {balance:,} VNĐ")

if __name__ == "__main__":
    while True:
        play_game()
        if input("\nChơi tiếp? (c/k): ").lower() != 'c': break
