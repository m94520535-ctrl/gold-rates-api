from flask import Flask, jsonify, request, render_template_string
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('rates.db')
    conn.row_factory = sqlite3.Row
    return conn

# 1. API لجلب الأسعار لتطبيق Flutter
@app.route('/get_rates', methods=['GET'])
def get_rates():
    conn = get_db_connection()
    rates_data = conn.execute('SELECT currency_key, rate_value FROM exchange_rates').fetchall()
    conn.close()

    rates = {row['currency_key']: row['rate_value'] for row in rates_data}
    
    return jsonify({
        "success": True,
        "rates": rates
    })

# 2. لوحة تحكم بسيطة لتحديث الأسعار من المتصفح
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    conn = get_db_connection()
    message = ""
    
    if request.method == 'POST':
        aden_rate = request.form.get('aden_rate')
        sanaa_rate = request.form.get('sanaa_rate')
        
        if aden_rate and sanaa_rate:
            conn.execute("UPDATE exchange_rates SET rate_value = ? WHERE currency_key = 'aden_rate'", (aden_rate,))
            conn.execute("UPDATE exchange_rates SET rate_value = ? WHERE currency_key = 'sanaa_rate'", (sanaa_rate,))
            conn.commit()
            message = "تم تحديث الأسعار بنجاح!"

    rates_data = conn.execute('SELECT currency_key, rate_value FROM exchange_rates').fetchall()
    conn.close()
    rates = {row['currency_key']: row['rate_value'] for row in rates_data}

    # صفحة HTML بسيطة للوحة التحكم
    html = f'''
    <!DOCTYPE html>
    <html dir="rtl">
    <head>
        <title>لوحة التحكم بالأسعار</title>
        <style>
            body {{ font-family: Arial; background: #111; color: #fff; text-align: center; padding: 50px; }}
            input {{ padding: 10px; margin: 10px; width: 200px; text-align: center; }}
            button {{ padding: 10px 20px; background: gold; border: none; cursor: pointer; font-weight: bold; }}
            .msg {{ color: lightgreen; margin-bottom: 20px; }}
        </style>
    </head>
    <body>
        <h2>لوحة تحديث أسعار الصرف</h2>
        {f'<div class="msg">{message}</div>' if message else ''}
        <form method="POST">
            <label>صرف عدن:</label><br>
            <input type="number" step="0.1" name="aden_rate" value="{rates.get('aden_rate', 1600.0)}"><br>
            <label>صرف صنعاء:</label><br>
            <input type="number" step="0.1" name="sanaa_rate" value="{rates.get('sanaa_rate', 535.0)}"><br>
            <button type="submit">حفظ التغييرات</button>
        </form>
    </body>
    </html>
    '''
    return render_template_string(html)

if __name__ == '__main__':
    app.run(debug=True, port=5000)