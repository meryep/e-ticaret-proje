import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score

print("Makine Öğrenmesi Modeli Hazırlanıyor...\n")

# 1. Veriyi Yükleme
df = pd.read_csv("data/master_analiz_tablosu.csv")

# Analizi en çok satan kategorilerden biri olan 'health_beauty' üzerine kuralım
df_kategori = df[df["product_category_name_english"] == "health_beauty"].copy()

# 2. Veriyi Günlük Bazda Toplulaştırma (Aggregation)
# Modelin satır satır siparişleri değil, "günlük toplam talebi" tahmin etmesi gerekir
gunluk_talep = (
    df_kategori.groupby("satis_tarihi")
    .agg(
        talep_adedi=(
            "order_id",
            "count",
        ),  # O günkü toplam sipariş sayısı (Hedef Değişken)
        ortalama_fiyat_usd=("fiyat_usd", "mean"),  # O günkü ortalama ürün fiyatı
        dolar_kuru=("dolar_kuru", "mean"),  # O günkü dolar kuru
        tufe_endeksi=("tufe_endeksi", "mean"),  # O ayki enflasyon
    )
    .dropna()
    .reset_index()
)

# 3. Bağımsız Değişkenler (X) ve Hedef Değişken (y) Ayrımı
X = gunluk_talep[["ortalama_fiyat_usd", "dolar_kuru", "tufe_endeksi"]]
y = gunluk_talep["talep_adedi"]

# Veriyi %80 Eğitim, %20 Test olarak ayırma
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 4. Model Eğitimi (Random Forest Regressor)
print("Random Forest Modeli Eğitiliyor...")
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 5. Tahmin ve Başarı Metrikleri
y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"\nModel Başarısı (R-Kare): {r2:.2f}")
print(f"Ortalama Mutlak Hata (MAE): Günlük {mae:.2f} adet sipariş sapması")

# 6. Hangi Makroekonomik Değişken Daha Önemli? (Feature Importance)
onem_dereceleri = pd.DataFrame(
    {"Değişken": X.columns, "Önem (%)": np.round(model.feature_importances_ * 100, 2)}
).sort_values(by="Önem (%)", ascending=False)

print("\nKozmetik Talebi Üzerindeki En Etkili Faktörler:")
print(onem_dereceleri.to_string(index=False))
