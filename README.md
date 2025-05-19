# 📊 Analisis Tren Penyewaan Sepeda dengan Streamlit

Dashboard interaktif ini dibuat menggunakan **Streamlit** untuk menganalisis data penyewaan sepeda dari dataset Bike Sharing tahun 2011-2012. Visualisasi yang disajikan membantu memahami pola penyewaan sepeda berdasarkan faktor waktu, musim, hari kerja, dan kondisi lingkungan.

---

## 📂 Isi Dataset

- **clean_day.csv** : Dataset harian yang sudah dibersihkan, berisi data penyewaan sepeda per hari dengan fitur seperti musim, hari kerja, cuaca, suhu, dan lain-lain.
- **clean_hour.csv** : Dataset penyewaan sepeda per jam untuk analisis tren waktu dalam sehari.

---

## 🛠️ Teknologi dan Library

- Python 3.x  
- [Streamlit](https://streamlit.io/) — pembuatan dashboard interaktif  
- [Pandas](https://pandas.pydata.org/) — pengolahan data  
- [Matplotlib](https://matplotlib.org/) & [Seaborn](https://seaborn.pydata.org/) — visualisasi data  
- [Numpy](https://numpy.org/) — manipulasi data numerik

---

## ⚙️ Fitur Utama Dashboard

1. **Filter Data**  
   - Pilihan Tahun: Semua Tahun, 2011, atau 2012  
   - Pilihan Kategori Waktu: Pagi, Siang, Sore, Malam (multiselect)

2. **Ringkasan Data**  
   Menjelaskan konteks dan informasi dasar dataset.

3. **Analisis Penyewaan Berdasarkan Bulan**  
   Grafik batang total penyewaan per bulan, dipisahkan berdasarkan tahun.

4. **Dampak Musim terhadap Penyewaan**  
   Grafik batang total penyewaan berdasarkan musim (Musim Semi, Panas, Gugur, Dingin).

5. **Tren Penyewaan Berdasarkan Jam**  
   Grafik garis jumlah penyewaan per jam dalam sehari.

6. **Korelasi Antar Faktor**  
   Heatmap korelasi antar variabel numerik penting seperti suhu, kecepatan angin, dan jumlah penyewaan.

7. **Pengaruh Hari Kerja dan Akhir Pekan**  
   Perbandingan total penyewaan sepeda antara hari kerja dan akhir pekan.

8. **Pola Penyewaan Berdasarkan Kategori Waktu (Clustering)**  
   Grafik batang total penyewaan berdasarkan kategori waktu (Pagi, Siang, Sore, Malam) sesuai filter pengguna.

---

## 🚀 Cara Menjalankan

1. Pastikan Python 3.x sudah terpasang di komputer Anda.  
2. Install library yang dibutuhkan:  
   ```bash
   pip install streamlit pandas matplotlib seaborn numpy
3. Jalankan aplikasi dengan perintah:
   ```cmd
   streamlit run app.py
