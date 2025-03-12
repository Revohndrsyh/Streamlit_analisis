import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load dataset yang sudah dibersihkan
day_df = pd.read_csv("clean_day.csv")
hour_df = pd.read_csv("clean_hour.csv")

# Mengubah format kolom tanggal menjadi datetime
day_df['dteday'] = pd.to_datetime(day_df['dteday'])

# Menghapus kolom non-numerik sebelum korelasi
day_df_numeric = day_df.select_dtypes(include=[np.number])

# Dashboard
st.title("📊 Analisis Tren Penyewaan Sepeda")

# Menambahkan sidebar untuk interaktivitas
st.sidebar.header("🔍 Filter Data")
selected_year = st.sidebar.radio("Pilih Tahun:", ["Semua Tahun", 2011, 2012])
selected_time = st.sidebar.multiselect("Pilih Kategori Waktu:", ['Pagi', 'Siang', 'Sore', 'Malam'], default=['Pagi', 'Siang', 'Sore', 'Malam'])

# Menyesuaikan dataset dengan filter yang dipilih
if selected_year != "Semua Tahun":
    day_df = day_df[day_df['yr'] == (selected_year - 2011)]

# Informasi Umum Dataset
st.subheader("📌 Ringkasan Data")
st.write("Saya menggunakan Bike Sharing Dataset untuk melihat penyewaan sepeda berdasarkan faktor-faktor seperti musim, hari kerja/akhir pekan, dan perkiraan per bulan. Data set ini diambil pada tahun 2011 hingga 2012")

# Tren Penyewaan Sepeda per Bulan
st.subheader("📈 Penyewaan Sepeda Berdasarkan Bulan")
rent_month = day_df.groupby(['yr', 'mnth'])['cnt'].sum().reset_index()
rent_month['yr'] = rent_month['yr'].map({0: 2011, 1: 2012})
fig, ax = plt.subplots()
sns.barplot(x='mnth', y='cnt', hue='yr', data=rent_month, ax=ax)
ax.set_ylabel("Jumlah Penyewaan")
ax.set_xlabel("Bulan")
st.pyplot(fig)

st.write("\n📌 **Analisis Penyewaan Sepeda Berdasarkan Bulan:**")
st.write(" 🔹 Bulan dengan jumlah penyewaan tertinggi: 9 2012 dengan 218573 penyewaan.")
st.write(" 🔹 Bulan dengan jumlah penyewaan terendah: 1 2011 dengan 38189 penyewaan.")

# Pengaruh Musim terhadap Penyewaan
st.subheader("🌦️ Dampak Musim terhadap Penyewaan")

# Mapping angka musim ke nama musim
season_mapping = {1: "Musim Semi", 2: "Musim Panas", 3: "Musim Gugur", 4: "Musim Dingin"}
day_df["season"] = day_df["season"].map(season_mapping)

# Membuat visualisasi
# Mengelompokkan data berdasarkan musim
rent_season = day_df.groupby('season')['cnt'].sum().reset_index()
palette_name = "viridis"
fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(x='season', y='cnt', data=rent_season, palette=palette_name, ax=ax)
# Mengatur format angka pada sumbu Y agar tidak dalam bentuk eksponensial
ax.ticklabel_format(style='plain', axis='y')
ax.set_ylabel("Total Penyewaan")
ax.set_xlabel("Musim")
ax.set_title("Dampak Musim terhadap Penyewaan", fontsize=14, fontweight="bold")
st.pyplot(fig)

st.write("\n📌 **Analisis Pengaruh Musim terhadap Penyewaan:**")
st.write("- Musim panas memiliki jumlah penyewaan tertinggi, menunjukkan bahwa cuaca lebih hangat meningkatkan minat pengguna untuk bersepeda.")
st.write("- Musim dingin memiliki penyewaan yang lebih rendah, mungkin disebabkan oleh kondisi cuaca yang kurang mendukung seperti suhu dingin atau hujan.")

# Tren Penyewaan Sepeda per Jam
st.subheader("⏰ Tren Penyewaan Sepeda Berdasarkan Waktu")
rent_hour = hour_df.groupby('hr')['cnt'].sum().reset_index()
fig, ax = plt.subplots()
sns.lineplot(x='hr', y='cnt', data=rent_hour, marker='o', ax=ax)
ax.set_ylabel("Jumlah Penyewaan")
st.pyplot(fig)

st.write("\n📌 **Analisis Tren Penyewaan Sepeda Berdasarkan Waktu:**")
st.write("Pola penyewaan sepeda menunjukkan dua puncak utama pada hari kerja:")
st.write("- **Pagi (07:00 - 09:00)**: Kemungkinan besar disebabkan oleh pengguna yang pergi ke tempat kerja atau sekolah.")
st.write("- **Sore (17:00 - 19:00)**: Diperkirakan banyak digunakan untuk perjalanan pulang kerja atau aktivitas sore.")
st.write("Pada akhir pekan, pola penyewaan lebih merata sepanjang hari.")

# Heatmap Korelasi Antar Variabel
st.subheader("🔍 Korelasi Antar Faktor")
# Mapping balik season ke angka agar bisa digunakan dalam korelasi
season_reverse_mapping = {"Musim Semi": 1, "Musim Panas": 2, "Musim Gugur": 3, "Musim Dingin": 4}
day_df["season"] = day_df["season"].map(season_reverse_mapping)
corr_columns = ['registered', 'casual', 'temp', 'atemp', 'yr', 'season', 'mnth', 'weekday',
                'workingday', 'holiday', 'hum', 'windspeed', 'weathersit', 'cnt']
day_df_numeric = day_df[corr_columns].select_dtypes(include=[np.number])
corr_matrix = day_df_numeric.corr()
fig, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="coolwarm", ax=ax)
st.pyplot(fig)

st.write("\n📌 **Analisis Korelasi Faktor Penyewaan Sepeda:**")
st.write("- **Jumlah pelanggan terdaftar** memiliki korelasi tertinggi (**0.95**) dengan penyewaan, menunjukkan bahwa pelanggan tetap adalah pengguna utama.")
st.write("- **Suhu (temp & atemp)** memiliki korelasi positif (**0.63**), yang berarti cuaca lebih hangat meningkatkan penyewaan.")
st.write("- **Kecepatan angin** memiliki korelasi negatif (**-0.23**), artinya semakin kencang angin, semakin sedikit penyewaan.")
st.write("- **Kondisi cuaca buruk** (hujan, kabut, atau salju) menurunkan jumlah penyewaan.")

# Visualiasi Pengaruh Hari Kerja dan Akhir Pekan terhadap Penyewaan
st.subheader("📅 Pengaruh Hari Kerja dan Akhir Pekan terhadap Penyewaan")
# difilter berdasarkan tahun yang dipilih
if selected_year != "Semua Tahun":
    day_df_filtered = day_df[day_df['yr'] == (selected_year - 2011)].copy()
else:
    day_df_filtered = day_df.copy()
# Mapping ulang nilai 0 = Akhir Pekan, 1 = Hari Kerja setelah filtering
workingday_mapping = {0: "Akhir Pekan", 1: "Hari Kerja"}
day_df_filtered["workingday"] = day_df_filtered["workingday"].map(workingday_mapping)
# Kelompokkan data berdasarkan hari kerja vs akhir pekan
rent_workingday = day_df_filtered.groupby('workingday')['cnt'].sum().reset_index()
# Ubah jumlah penyewaan ke dalam skala juta
rent_workingday["cnt"] = rent_workingday["cnt"] / 1_000_000  
rent_workingday["cnt"] = rent_workingday["cnt"].round(1)  
fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(x='workingday', y='cnt', data=rent_workingday, palette="coolwarm", ax=ax)
ax.set_ylabel("Total Penyewaan (Juta)", fontsize=12)  # Menunjukkan bahwa datanya dalam juta
ax.set_xlabel("Kategori Hari", fontsize=12)
ax.set_title("Perbandingan Penyewaan Sepeda pada Hari Kerja dan Akhir Pekan", fontsize=14, fontweight="bold")
st.pyplot(fig)


st.write("\n📌 **Analisis Penyewaan Sepeda Berdasarkan Hari Kerja dan Akhir Pekan:**")
st.write("- **Hari kerja memiliki jumlah penyewaan yang lebih tinggi**, terutama karena penggunaan sepeda untuk transportasi ke tempat kerja atau sekolah.")
st.write("- **Akhir pekan memiliki penyewaan yang lebih rendah**, namun masih cukup tinggi karena digunakan untuk aktivitas rekreasi atau olahraga.")
st.write("- **Perbedaan pola ini penting** untuk memahami bagaimana layanan sepeda dapat disesuaikan untuk memenuhi kebutuhan harian vs rekreasi.")

# Clustering Manual Berdasarkan Waktu Penyewaan
st.subheader("📊 Pola Penyewaan Berdasarkan Kategori Waktu (Clustering)")
def categorize_time(hour):
    if 6 <= hour < 12:
        return 'Pagi'
    elif 12 <= hour < 18:
        return 'Siang'
    elif 18 <= hour < 24:
        return 'Sore'
    else:
        return 'Malam'

hour_df['time_category'] = hour_df['hr'].apply(categorize_time)
clustering_df = hour_df.groupby(['time_category']).agg(
    Total_Usage=('cnt', 'sum'),
    Avg_Usage=('cnt', 'mean')
).reset_index()

# Filter data berdasarkan input user
clustering_df = clustering_df[clustering_df['time_category'].isin(selected_time)]

fig, ax = plt.subplots()
sns.barplot(x='time_category', y='Total_Usage', data=clustering_df, palette="coolwarm", ax=ax)
ax.set_ylabel("Total Penyewaan")
st.pyplot(fig)

st.write("\n🔹 **Siang hari memiliki penggunaan tertinggi**, menunjukkan aktivitas tertinggi pada jam kerja atau jam makan siang.")
st.write("🔹 **Sore hari** juga memiliki jumlah penyewaan tinggi, yang kemungkinan besar digunakan oleh pekerja setelah jam kerja.")
st.write("🔹 **Malam hari memiliki penggunaan terendah**, yang bisa disebabkan oleh faktor keamanan atau berkurangnya mobilitas masyarakat pada malam hari.")

st.caption("MC254D5Y0860 - Revo Hendriansyah")
