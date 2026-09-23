import pandas as pd

df_orders = pd.read_csv("data/olist_orders_dataset.csv")

# Tarih içeren sütunların listesi
date_columns = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date",
]

# Tüm tarih sütunlarını standart datetime formatına dönüştürme
for col in date_columns:
    df_orders[col] = pd.to_datetime(df_orders[col])

print("Orijinal Başlangıç Tarihi:", df_orders["order_purchase_timestamp"].min())
print("Orijinal Bitiş Tarihi:", df_orders["order_purchase_timestamp"].max())

# Veri setindeki en eski tarih
min_date_original = df_orders["order_purchase_timestamp"].min()

# Hedef başlangıç tarihi (1 Ocak 2024, 00:00:00)
target_start_date = pd.to_datetime("2024-01-01 00:00:00")

# Aradaki statik zaman farkını hesaplama
time_shift_delta = target_start_date - min_date_original

print(f"Uygulanacak Zaman Kayması: {time_shift_delta}")

# Zaman farkını tüm ilgili sütunlara vektörel olarak ekleme
for col in date_columns:
    df_orders[col] = df_orders[col] + time_shift_delta

print("\nGüncellenmiş Başlangıç Tarihi:", df_orders["order_purchase_timestamp"].min())
print("Güncellenmiş Bitiş Tarihi:", df_orders["order_purchase_timestamp"].max())

# Dönüşümü doğrulamak için ilk 5 satırın tarih sütunlarını inceleme
print(df_orders[date_columns].head())

# Güncellenmiş veriyi index sütunu oluşturmadan yeni bir dosya olarak kaydetme
df_orders.to_csv("data/olist_orders_dataset_shifted.csv", index=False)
print("Zaman kaydırma işlemi tamamlandı ve dosya kaydedildi.")
