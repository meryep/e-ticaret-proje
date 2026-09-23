import sqlite3

# Veritabanı dosyasını oluştur (veya varsa bağlan)
conn = sqlite3.connect("eticaret_analiz.db")
cursor = conn.cursor()

# Satış verilerini tutacağımız ilk tablomuz
cursor.execute("""
CREATE TABLE IF NOT EXISTS Satislar (
    islem_id INTEGER PRIMARY KEY AUTOINCREMENT,
    urun_kategorisi TEXT,
    birim_fiyat REAL,
    satis_miktari INTEGER,
    islem_tarihi DATE
)
""")

conn.commit()
conn.close()
print("E-ticaret veritabanı ve Satışlar tablosu başarıyla oluşturuldu!")
