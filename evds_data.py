import os
import evds
import pandas as pd
from dotenv import load_dotenv

# API anahtarını yükle
load_dotenv()
api_key = os.getenv("EVDS_API_KEY")
evds_api = evds.evdsAPI(api_key)

# TÜFE (Tüketici Fiyat Endeksi) Seri Kodu ve Tarih Aralığı
seri_kodu = "TP.FG.J0"
baslangic_tarihi = "01-01-2024"
bitis_tarihi = "31-12-2026"

print("EVDS üzerinden TÜFE verisi çekiliyor...")

try:
    # Veriyi çekme işlemi
    df_tufe = evds_api.get_data(
        [seri_kodu], startdate=baslangic_tarihi, enddate=bitis_tarihi
    )

    # Sütun isimlerini SQL'de ve Pandas'ta kolay çalışılacak şekilde temizleme
    df_tufe.rename(
        columns={"Tarih": "ay_yil", "TP_FG_J0": "tufe_endeksi"}, inplace=True
    )

    # EVDS '2024-1' gibi gelen tarihi standart YYYY-MM-01 datetime formatına çevirme
    df_tufe["ay_yil"] = pd.to_datetime(df_tufe["ay_yil"], format="%Y-%m")

    # İleride birleştirme yapabilmek için 'Yıl' ve 'Ay' sütunları ekleyelim
    df_tufe["yil"] = df_tufe["ay_yil"].dt.year
    df_tufe["ay"] = df_tufe["ay_yil"].dt.month

    # 'data' klasörüne kaydet
    dosya_yolu = "data/tufe_2024_2026.csv"
    df_tufe.to_csv(dosya_yolu, index=False)

    print(f"TÜFE verisi başarıyla çekildi ve {dosya_yolu} konumuna kaydedildi.")
    print("\nVerinin ilk 5 satırı:")
    print(df_tufe.head())

except Exception as e:
    print(f"Veri çekerken bir hata oluştu: {e}")
