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
    user_choice = data.get('choice') # '1', '2', '3', '4'
    
    current_balance = wallet.get_balance()
    if bet > current_balance:
        return jsonify({"error": "Không đủ tiền!"}), 400

    # 1. Gọi generator.py tạo số
    secret_num = generator.generate_number()
    
    # 2. Xử lý logic thắng thua
    a, b = int(secret_num[0]), int(secret_num[1])
    d = (a + b) % 10
    
    is_tai = 0 <= d <= 4
    is_chan = d in [0, 2, 4, 6, 8]
    
    win = False
    if user_choice == '1' and is_tai: win = True
    elif user_choice == '2' and not is_tai: win = True
    elif user_choice == '3' and is_chan: win = True
    elif user_choice == '4' and not is_chan: win = True

    # 3. Cập nhật ví bằng wallet.py và lưu bằng storage.py
    new_balance = current_balance + bet if win else current_balance - bet
    wallet.update_balance(new_balance)
    storage.save_current_round(secret_num)
    storage.log_history("Web", secret_num, bet, user_choice, "THẮNG" if win else "THUA", new_balance)

    return jsonify({
        "number": secret_num,
        "tong": a + b,
        "don_vi": d,
        "win": win,
        "new_balance": new_balance
    })

if __name__ == '__main__':
    app.run(debug=True)
