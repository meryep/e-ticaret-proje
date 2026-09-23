import yfinance as yf
import pandas as pd

print("Yahoo Finance üzerinden günlük Dolar kuru çekiliyor...")

try:
    # USD/TRY paritesi (Eğer projenin aslına sadık kalıp Brezilya Reali kullanmak isterseniz 'BRL=X' yapabilirsiniz)
    doviz_kodu = "TRY=X"

    # 2024-2026 aralığı için veriyi çekme
    kur_verisi = yf.download(doviz_kodu, start="2024-01-01", end="2026-12-31")

    # Sadece 'Close' (Kapanış) fiyatını alıp index'i sıfırlama
    df_kur = kur_verisi[["Close"]].reset_index()

    # Sütun isimlerini veritabanı ve birleştirme işlemleri için standartlaştırma
    df_kur.columns = ["tarih", "dolar_kuru"]

    # Sadece YYYY-MM-DD kısmını tutacak şekilde tarihi temizleme
    df_kur["tarih"] = pd.to_datetime(df_kur["tarih"]).dt.date

    # 'data' klasörüne kaydetme
    dosya_yolu = "data/dolar_kuru_2024_2026.csv"
    df_kur.to_csv(dosya_yolu, index=False)

    print(f"Dolar kuru başarıyla çekildi ve {dosya_yolu} konumuna kaydedildi.")
    print("\nVerinin ilk 5 satırı:")
    print(df_kur.head())

except Exception as e:
    print(f"Veri çekerken bir hata oluştu: {e}")
