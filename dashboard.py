import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load dataset yang sudah dibersihkan
day_df = pd.read_csv("clean_day.csv")
hour_df = pd.read_csv("clean_hour.csv")
rfm_df = pd.read_csv("rfm_analysis.csv")

# Mengubah format kolom tanggal menjadi datetime
day_df['dteday'] = pd.to_datetime(day_df['dteday'])

# Menghapus kolom non-numerik sebelum korelasi
day_df_numeric = day_df.select_dtypes(include=[np.number])

# Dashboard
st.title("📊 Analisis Tren Penyewaan Sepeda")

# Informasi Umum Dataset
st.subheader("📌 Ringkasan Data")
st.write("Saya menggunakan Bike Sharing Dataset untuk melihat penyewaan sepeda berdasarkan fakor-fakor seperti musim, hari kerja/akhir pekan, dan perkiraan perbulan. data set ini diambil pada tahun 2011 hingga 2012")

# Tren Penyewaan Sepeda per Bulan
st.subheader("📈 Penyewaan Sepeda Berdasarkan Bulan")
rent_month = day_df.groupby(['yr', 'mnth'])['cnt'].sum().reset_index()
rent_month['yr'] = rent_month['yr'].map({0: 2011, 1: 2012})
fig, ax = plt.subplots()
sns.barplot(x='mnth', y='cnt', hue='yr', data=rent_month, ax=ax)
ax.set_ylabel("Jumlah Penyewaan")
ax.set_xlabel("Bulan")
st.pyplot(fig)

# Menampilkan bulan dengan penyewaan tertinggi dan terendah
top_month = rent_month.loc[rent_month['cnt'].idxmax()]
low_month = rent_month.loc[rent_month['cnt'].idxmin()]
st.write(f"🔹 Bulan dengan jumlah penyewaan tertinggi: **{top_month['mnth']} {int(top_month['yr'])}** dengan **{top_month['cnt']}** penyewaan.")
st.write(f"🔹 Bulan dengan jumlah penyewaan terendah: **{low_month['mnth']} {int(low_month['yr'])}** dengan **{low_month['cnt']}** penyewaan.")

# Pengaruh Musim terhadap Penyewaan
st.subheader("🌦️ Dampak Musim terhadap Penyewaan")
rent_season = day_df.groupby('season')['cnt'].sum().reset_index()
fig, ax = plt.subplots()
sns.barplot(x='season', y='cnt', data=rent_season, ax=ax)
ax.set_ylabel("Total Penyewaan")
st.pyplot(fig)
st.write("Musim memiliki pengaruh besar terhadap jumlah penyewaan sepeda. Penyewaan cenderung meningkat selama musim panas dan menurun di musim dingin.")

# Penyewaan pada Hari Kerja vs Akhir Pekan
st.subheader("📅 Pola Penyewaan di Hari Kerja dan Akhir Pekan")
rent_by_category = day_df.groupby('day_category')['cnt'].sum().reset_index()
fig, ax = plt.subplots()
sns.barplot(data=rent_by_category, x="day_category", y="cnt", palette="coolwarm", ax=ax)
ax.set_ylabel("Jumlah Penyewaan")
st.pyplot(fig)
st.write("Penyewaan sepeda lebih tinggi pada hari kerja, menunjukkan bahwa sepeda lebih sering digunakan sebagai alat transportasi dibandingkan hanya untuk rekreasi.")

# Tren Penyewaan Sepeda per Jam
st.subheader("⏰ Tren Penyewaan Sepeda Berdasarkan Waktu")
rent_hour = hour_df.groupby('hr')['cnt'].sum().reset_index()
fig, ax = plt.subplots()
sns.lineplot(x='hr', y='cnt', data=rent_hour, marker='o', ax=ax)
ax.set_ylabel("Jumlah Penyewaan")
st.pyplot(fig)
st.write("Pola penyewaan menunjukkan dua puncak utama pada hari kerja: pagi (07:00 - 09:00) dan sore (17:00 - 19:00). Pada akhir pekan, penyewaan lebih merata sepanjang hari.")

# Heatmap Korelasi Antar Variabel
st.subheader("🔍 Korelasi Antar Faktor")
corr_columns = ['registered', 'casual', 'temp', 'atemp', 'yr', 'season', 'mnth', 'weekday', 'workingday', 'holiday', 'hum', 'windspeed', 'weathersit', 'cnt']
corr_matrix = day_df[corr_columns].corr()
fig, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="coolwarm", ax=ax)
st.pyplot(fig)

# Faktor yang Mempengaruhi Penyewaan Sepeda
st.subheader("📊 Faktor Utama dalam Penyewaan Sepeda")
st.write("**Faktor Positif:**")
st.write("- **Jumlah pelanggan terdaftar** memiliki korelasi tertinggi (**0.95**) dengan penyewaan, yang menunjukkan bahwa pelanggan tetap adalah pengguna utama.")
st.write("- **Suhu (temp & atemp)** memiliki korelasi positif (**0.63**), yang berarti cuaca lebih hangat meningkatkan penyewaan.")

st.write("**Faktor Negatif:**")
st.write("- **Kecepatan angin** memiliki korelasi negatif (**-0.23**), artinya semakin kencang angin, semakin sedikit penyewaan.")
st.write("- **Kondisi cuaca buruk** (hujan, kabut, atau salju) menurunkan jumlah penyewaan.")

# Visualisasi Distribusi RFM
st.subheader("📊 Pola Pelanggan Berdasarkan Analisis RFM")
fig, axes = plt.subplots(1, 3, figsize=(15, 5))

# Recency
sns.histplot(rfm_df['Recency'], bins=20, kde=True, ax=axes[0], color="blue")
axes[0].set_title("Distribusi Recency")
axes[0].set_xlabel("Hari sejak transaksi terakhir")
axes[0].set_ylabel("Jumlah Pelanggan")

# Frequency
sns.histplot(rfm_df['Frequency'], bins=10, kde=True, ax=axes[1], color="green")
axes[1].set_title("Distribusi Frequency")
axes[1].set_xlabel("Jumlah Transaksi")
axes[1].set_ylabel("Jumlah Pelanggan")

# Monetary
sns.histplot(rfm_df['Monetary'], bins=10, kde=True, ax=axes[2], color="red")
axes[2].set_title("Distribusi Monetary")
axes[2].set_xlabel("Total Penyewaan")
axes[2].set_ylabel("Jumlah Pelanggan")

plt.tight_layout()
st.pyplot(fig)

st.write("Analisis RFM menunjukkan bahwa sebagian besar pelanggan memiliki nilai Frequency dan Monetary yang rendah, menunjukkan perlunya strategi peningkatan retensi pelanggan.")
st.write("Strategi seperti **diskon untuk pelanggan lama** dan **langganan bulanan** dapat membantu meningkatkan keterlibatan pelanggan.")

st.caption("MC254D5Y0860 - Revo Hendriansyah")