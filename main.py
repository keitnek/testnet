from flask import Flask, render_template, request, jsonify
import generator
import wallet
import storage
import os

app = Flask(__name__)

@app.route('/')
def index():
    # Trả về giao diện HTML
    return render_template('index.html')

@app.route('/get_data', methods=['GET'])
def get_data():
    # Lấy số dư hiện tại từ wallet.py
    balance = wallet.get_balance()
    return jsonify({"balance": balance})

@app.route('/play', methods=['POST'])
def play():
    data = request.json
    bet = int(data.get('bet'))
    user_choice = data.get('choice')
    
    current_balance = wallet.get_balance()
    if bet > current_balance:
        return jsonify({"error": "Không đủ tiền!"}), 400

    secret_num = generator.generate_number()
    a, b = int(secret_num[0]), int(secret_num[1])
    d = (a + b) % 10
    
    # Logic thắng thua
    is_tai = 0 <= d <= 4
    is_chan = d % 2 == 0
    win = False
    if user_choice == '1' and is_tai: win = True
    elif user_choice == '2' and not is_tai: win = True
    elif user_choice == '3' and is_chan: win = True
    elif user_choice == '4' and not is_chan: win = True

    # --- ĐOẠN QUAN TRỌNG: CẬP NHẬT SỐ DƯ ---
    new_balance = current_balance + bet if win else current_balance - bet
    
    was_reset = False
    # Nếu tiền về 0 (hoặc âm), tự động hồi lại 1 triệu
    if new_balance <= 0:
        new_balance = 1000000
        was_reset = True

    wallet.update_balance(new_balance)
    storage.save_current_round(secret_num)
    storage.log_history("Web", secret_num, bet, user_choice, "THẮNG" if win else "THUA", new_balance)

    return jsonify({
        "number": secret_num,
        "tong": a + b,
        "don_vi": d,
        "win": win,
        "new_balance": new_balance,
        "was_reset": was_reset  # Gửi thêm thông tin này về giao diện
    })
