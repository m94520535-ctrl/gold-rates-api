import sqlite3

# إنشاء أو الاتصال بقاعدة البيانات الداخلية (ملف محلي)
conn = sqlite3.connect('rates.db')
cursor = conn.cursor()

# إنشاء جدول أسعار الصرف
cursor.execute('''
    CREATE TABLE IF NOT EXISTS exchange_rates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        currency_key TEXT UNIQUE NOT NULL,
        rate_value REAL NOT NULL
    )
''')

# إدراج الأسعار الافتراضية لعدن وصنعاء
cursor.execute("INSERT OR REPLACE INTO exchange_rates (currency_key, rate_value) VALUES ('aden_rate', 1600.0)")
cursor.execute("INSERT OR REPLACE INTO exchange_rates (currency_key, rate_value) VALUES ('sanaa_rate', 535.0)")

conn.commit()
conn.close()

print("تم إنشاء قاعدة البيانات بنجاح (rates.db)!")