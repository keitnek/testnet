import time
import generator
import wallet
import storage

def play_online():
    balance = wallet.get_balance()
    print(f"\n" + "═"*30)
    print(f"💰 VÍ ONLINE: {balance:,} VNĐ")
    print("═"*30)

    try:
        bet = int(input("💵 Nhập tiền cược: "))
        if bet > balance or bet <= 0:
            print("❌ Tiền không đủ!"); return
        
        print("1. Tài | 2. Xỉu | 3. Chẵn | 4. Lẻ")
        choice_idx = input("👉 Chọn (1-4): ")
        mapping = {"1": "Tài", "2": "Xỉu", "3": "Chẵn", "4": "Lẻ"}
        if choice_idx not in mapping: return
    except: return

    # --- HỆ THỐNG TỰ ĐỘNG ---
    print("\n🎲 Đang quay số...")
    time.sleep(1) # Giả lập chờ đợi cho kịch tính
    
    secret_num = generator.generate_number()
    storage.save_current_round(secret_num)

    # Logic thắng thua
    a, b = int(secret_num[0]), int(secret_num[1])
    d = (a + b) % 10
    is_tai = 0 <= d <= 4
    is_chan = d in [0, 2, 4, 6, 8]
    
    win = False
    if choice_idx == '1' and is_tai: win = True
    elif choice_idx == '2' and not is_tai: win = True
    elif choice_idx == '3' and is_chan: win = True
    elif choice_idx == '4' and not is_chan: win = True

    # Cập nhật kết quả
    balance = balance + bet if win else balance - bet
    wallet.update_balance(balance)
    res_text = "THẮNG 🎉" if win else "THUA 💀"
    
    print(f"🎯 KẾT QUẢ: {secret_num} ({a}+{b}={a+b})")
    print(f"📢 Đơn vị {d} -> {res_text}")
    print(f"💳 Số dư mới: {balance:,} VNĐ")

if __name__ == "__main__":
    while True:
        play_online()
        if input("\nChơi tiếp? (c/k): ").lower() != 'c': break
