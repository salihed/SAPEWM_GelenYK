import os
import pandas as pd
import locale

# Türkçe bindelik ayarlarını uygulama
locale.setlocale(locale.LC_ALL, 'tr_TR.utf8')

# Kullanıcı adını al
kullanici_adi = os.getlogin()

# Dosya yolunu oluşturma (Windows için)
dosya_yolu = f"C:/Users/{kullanici_adi}/Desktop/depoin.xlsx"

# Excel dosyasını okuma
df = pd.read_excel(dosya_yolu, engine='openpyxl')

# "Depo prosesi tipi tanımı" sütununda "Depolama" değerine sahip satırları filtreleme
depolama_df = df[df["Depo prosesi tipi tanımı"] == "Depolama"]

# "Kutu İçi Miktar" sütununda sayı verisi olmayan satırları ve bu değerin 0 olduğu satırları göz ardı etme
depolama_df = depolama_df[depolama_df["Kutu İçi Miktar"].notna() & (depolama_df["Kutu İçi Miktar"] != 0)]

# "Çkş.yr.hdf.mkt.TÖB" sütunundaki değeri "Kutu İçi Miktar" sütunu ile bölme ve kalanı bulma
depolama_df["Kalan"] = depolama_df["Çkş.yr.hdf.mkt.TÖB"] % depolama_df["Kutu İçi Miktar"]

# Birim ağırlık hesaplama
depolama_df["Birim ağırlık"] = depolama_df["Net ağırlık"] / depolama_df["Çkş.yr.hdf.mkt.TÖB"]

# Yarım kutu ağırlığını hesaplama
depolama_df["Yarım kutu ağırlığı"] = depolama_df["Kalan"] * depolama_df["Birim ağırlık"]

# Yarım kutu ağırlığının 17'den büyük olduğu satırları filtreleme
depolama_df = depolama_df[depolama_df["Yarım kutu ağırlığı"] <= 17]

# Yarım kutuların toplam net ağırlığı ve miktarı
toplam_yarim_kutu_agirligi = depolama_df["Yarım kutu ağırlığı"].sum().round(0)

print(f"Toplam yarım kutu miktarı: {depolama_df[depolama_df['Kalan'] != 0].shape[0]}")
print(f"Toplam yarım kutu ağırlığı: {locale.format_string('%d', toplam_yarim_kutu_agirligi, grouping=True)}")
