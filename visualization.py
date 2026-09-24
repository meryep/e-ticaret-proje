import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

print("Veri okunuyor ve grafikler hazırlanıyor...")

# Grafik stili ayarları
plt.style.use("seaborn-v0_8-darkgrid")

# 1. Veri Hazırlığı
df = pd.read_csv("data/master_analiz_tablosu.csv")
df_kategori = df[df["product_category_name_english"] == "health_beauty"].copy()

gunluk_talep = (
    df_kategori.groupby("satis_tarihi")
    .agg(
        talep_adedi=("order_id", "count"),
        ortalama_fiyat_usd=("fiyat_usd", "mean"),
        dolar_kuru=("dolar_kuru", "mean"),
        tufe_endeksi=("tufe_endeksi", "mean"),
    )
    .dropna()
    .reset_index()
)

gunluk_talep["satis_tarihi"] = pd.to_datetime(gunluk_talep["satis_tarihi"])

X = gunluk_talep[["ortalama_fiyat_usd", "dolar_kuru", "tufe_endeksi"]]
y = gunluk_talep["talep_adedi"]

# Zaman serisi olduğu için veriyi karıştırmadan (shuffle=False) bölüyoruz
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, shuffle=False
)

# 2. Model Eğitimi
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 3. Grafik 1: Değişken Önem Düzeyi (Feature Importance)
onem_dereceleri = pd.DataFrame(
    {
        "Değişken": ["Ortalama Fiyat (USD)", "Dolar Kuru", "TÜFE Endeksi (Enflasyon)"],
        "Önem Değeri": model.feature_importances_,
    }
).sort_values(by="Önem Değeri", ascending=False)

plt.figure(figsize=(10, 5))
sns.barplot(
    x="Önem Değeri",
    y="Değişken",
    data=onem_dereceleri,
    hue="Değişken",
    palette="viridis",
    legend=False,
)
plt.title(
    "Kozmetik Talebinde Makroekonomik Etkilerin Ağırlığı",
    fontsize=14,
    fontweight="bold",
)
plt.xlabel("Etki Oranı (%)")
plt.ylabel("")
plt.tight_layout()
plt.savefig("data/ozellik_onemi.png")
plt.show()

# 4. Grafik 2: Gerçekleşen vs. Tahmin Edilen (Zaman Serisi)
test_sonuclari = pd.DataFrame(
    {
        "Tarih": gunluk_talep.loc[X_test.index, "satis_tarihi"],
        "Gerçek Talep": y_test,
        "Model Tahmini": model.predict(X_test),
    }
)

plt.figure(figsize=(14, 6))
plt.plot(
    test_sonuclari["Tarih"],
    test_sonuclari["Gerçek Talep"],
    label="Gerçekleşen Talep",
    marker="o",
    alpha=0.6,
    color="steelblue",
)
plt.plot(
    test_sonuclari["Tarih"],
    test_sonuclari["Model Tahmini"],
    label="Model Tahmini",
    marker="x",
    alpha=0.9,
    color="darkred",
    linestyle="--",
)
plt.title(
    "Test Verisinde Gerçekleşen Satışlar ve Modelin Tahminleri",
    fontsize=14,
    fontweight="bold",
)
plt.xlabel("Tarih")
plt.ylabel("Günlük Sipariş Adedi")
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("data/tahmin_zaman_serisi.png")
plt.show()
