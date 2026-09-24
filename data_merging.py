import pandas as pd

print("Veri birleştirme işlemi başlıyor...\n")

# 1. Verileri Okuma
df_orders = pd.read_csv("data/olist_orders_dataset_shifted.csv")
df_items = pd.read_csv("data/olist_order_items_dataset.csv")
df_products = pd.read_csv("data/olist_products_dataset.csv")
df_translation = pd.read_csv("data/product_category_name_translation.csv")
df_kur = pd.read_csv("data/dolar_kuru_2024_2026.csv")
df_tufe = pd.read_csv("data/tufe_2024_2026.csv")

# 2. Tarih Formatlarını Ayarlama
df_orders["order_purchase_timestamp"] = pd.to_datetime(
    df_orders["order_purchase_timestamp"]
)
df_orders["satis_tarihi"] = df_orders["order_purchase_timestamp"].dt.date.astype(str)
df_orders["satis_yili"] = df_orders["order_purchase_timestamp"].dt.year
df_orders["satis_ayi"] = df_orders["order_purchase_timestamp"].dt.month
df_kur["tarih"] = df_kur["tarih"].astype(str)

# 3. E-Ticaret Tablolarını Birleştirme (JOIN)
master_df = pd.merge(df_orders, df_items, on="order_id", how="inner")
master_df = pd.merge(master_df, df_products, on="product_id", how="left")
master_df = pd.merge(master_df, df_translation, on="product_category_name", how="left")

# 4. Makroekonomik Verileri Entegre Etme
master_df = pd.merge(
    master_df, df_kur, left_on="satis_tarihi", right_on="tarih", how="left"
)
master_df = pd.merge(
    master_df,
    df_tufe,
    left_on=["satis_yili", "satis_ayi"],
    right_on=["yil", "ay"],
    how="left",
)

# 5. Özellik Mühendisliği (Feature Engineering)
master_df.drop(columns=["tarih", "yil", "ay"], inplace=True, errors="ignore")

# Hafta sonu ve tatillerde kur verisi 'NaN' döneceği için bir önceki iş gününün kurunu ileriye kopyalıyoruz (Forward Fill)
master_df["dolar_kuru"] = master_df["dolar_kuru"].ffill()

# Dolar kuru üzerinden reel fiyat hesaplaması
master_df["fiyat_usd"] = master_df["price"] / master_df["dolar_kuru"]

# 6. Sonucu Kaydetme
cikis_yolu = "data/master_analiz_tablosu.csv"
master_df.to_csv(cikis_yolu, index=False)

print(f"İşlem Başarılı! Toplam Satır Sayısı: {len(master_df)}")
print(f"Bütünleşik veri seti '{cikis_yolu}' olarak kaydedildi.\n")
print("Oluşan Yeni Tablonun İlk 5 Satırı (Hedef Sütunlar):")
print(
    master_df[
        [
            "order_id",
            "product_category_name_english",
            "price",
            "dolar_kuru",
            "fiyat_usd",
            "tufe_endeksi",
        ]
    ].head()
)
