import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

# Set Page Config
st.set_page_config(page_title="E-commerce Data Dashboard", layout="wide")

# Helper function untuk memuat data
def load_data():
    # Pastikan file CSV ini ada di folder yang sama dengan dashboard.py
    monthly_df = pd.read_csv("monthly_revenue_clean.csv")
    city_df = pd.read_csv("city_revenue_clean.csv")
    rfm_df = pd.read_csv("rfm_clean.csv") 
    
    monthly_df['order_purchase_timestamp'] = pd.to_datetime(monthly_df['order_purchase_timestamp'])
    return monthly_df, city_df, rfm_df

# Memanggil data
monthly_revenue_df, city_revenue_df, rfm_df = load_data()

# --- SIDEBAR ---
with st.sidebar:
    st.title("Proyek Akhir Fundamental Analisis Data")
    
    # Membatasi rentang waktu sesuai dataset
    min_date = monthly_revenue_df["order_purchase_timestamp"].min()
    max_date = monthly_revenue_df["order_purchase_timestamp"].max()
    
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# --- FILTER DATA BERDASARKAN INPUT SIDEBAR ---
# Inilah langkah krusial agar dashboard dinamis (Pesan dari Reviewer)
main_df = monthly_revenue_df[
    (monthly_revenue_df["order_purchase_timestamp"] >= pd.to_datetime(start_date)) & 
    (monthly_revenue_df["order_purchase_timestamp"] <= pd.to_datetime(end_date))
]

# --- MAIN PAGE ---
st.title("📊 E-commerce Public Dashboard")

st.markdown("""
### **Tentang Dataset**
Dashboard ini menyajikan analisis mendalam dari **E-commerce Public Dataset**. Data difokuskan pada periode **2017 hingga 2018** untuk memahami tren pertumbuhan pendapatan dan distribusi geografis pelanggan guna mendukung keputusan strategis.
""")

st.markdown("---")

# 1. TREN PENDAPATAN BULANAN
st.subheader("Tren Pendapatan Bulanan")
fig, ax = plt.subplots(figsize=(14, 6))

# Menyiapkan Data DINAMIS (Menggunakan main_df hasil filter)
x_months = main_df['order_purchase_timestamp'].dt.strftime('%b %Y')  
y_revenue = main_df['revenue'] / 1_000_000

ax.plot(
    x_months, 
    y_revenue, 
    marker='o', 
    markersize=8,
    linewidth=2.5, 
    color='#2E7D32',
    markerfacecolor='white',
    markeredgewidth=2
)

# Mengatur Grid & Label
ax.grid(axis='y', linestyle='--', alpha=0.3)
ax.grid(axis='x', linestyle=':', alpha=0.5)

ax.set_title("Tren Pendapatan Bulanan Periode 2017 - 2018", loc="left", fontsize=16, pad=25)
ax.set_xlabel("Bulan Pembelian", fontsize=12, labelpad=15)
ax.set_ylabel("Total Pendapatan (Juta BRL)", fontsize=12, labelpad=15)

plt.xticks(rotation=45, ha='right', fontsize=10)

# Spines removal
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

ax.set_ylim(bottom=-0.05) 

st.pyplot(fig)

st.info("""
**Insight Tren Pendapatan (2017-2018):**
* Pendapatan menunjukkan tren akselerasi yang kuat sejak awal 2017. 
* Puncak performa tertinggi tercapai pada **November 2017**, melampaui **1.2 Juta BRL**.
* **Rekomendasi:** Perusahaan perlu meningkatkan kapasitas logistik pada bulan Oktober untuk mengantisipasi lonjakan musiman tahunan.
""")

st.markdown("---")

# 2. KOTA DENGAN PENDAPATAN TERTINGGI
st.subheader("10 Kota dengan Pendapatan Tertinggi")
fig_city, ax_city = plt.subplots(figsize=(12, 7))

# Kita tampilkan top 10 berdasarkan data statis kota (atau bisa kamu filter jika ada data tanggal di city_df)
sns.barplot(
    x="payment_value", 
    y="customer_city", 
    data=city_revenue_df.head(10), 
    color="#1976D2", 
    ax=ax_city
)

ax_city.set_title("10 Kota dengan Total Pendapatan Tertinggi (2017-2018)", loc="left", fontsize=14, pad=20)
ax_city.set_xlabel("Total Pendapatan (Ribu BRL)", fontsize=10)
ax_city.set_ylabel("Nama Kota", fontsize=10)

ax_city.spines['top'].set_visible(False)
ax_city.spines['right'].set_visible(False)

st.pyplot(fig_city)

st.info("""
**Insight Distribusi Geografis:**
* Kota **Sao Paulo** merupakan kontributor pendapatan terbesar secara mutlak.
* **Rekomendasi:** Perluasan titik distribusi (distribution center) di sekitar wilayah Sao Paulo untuk mempercepat waktu pengiriman.
""")

st.markdown("---")

# 3. RFM ANALYSIS
st.subheader("Distribusi Segmen Pelanggan (RFM)")
fig_rfm, ax_rfm = plt.subplots(figsize=(10, 6))

sns.countplot(
    x='customer_segment', 
    data=rfm_df, 
    palette='viridis', 
    order=["Top Customer", "High Value Customer", "Medium Value Customer", "Low Value Customer"],
    ax=ax_rfm
)

ax_rfm.set_title("Distribusi Segmen Pelanggan Berdasarkan Skor RFM", fontsize=14, pad=20)
ax_rfm.set_xlabel("Segmentasi Berdasarkan Skor RFM", fontsize=12, labelpad=20)
ax_rfm.set_ylabel("Jumlah Pelanggan", fontsize=12)

ax_rfm.spines['top'].set_visible(False)
ax_rfm.spines['right'].set_visible(False)

# Annotations
for p in ax_rfm.patches:
    ax_rfm.annotate(f'{int(p.get_height())}', 
                (p.get_x() + p.get_width() / 2., p.get_height()), 
                ha = 'center', va = 'center', 
                xytext = (0, 9), 
                textcoords = 'offset points',
                fontsize=10)

st.pyplot(fig_rfm)

st.info("""
**Insight Analisis RFM:**
* Mayoritas pelanggan adalah **Low Value Customer**.
* **Rekomendasi:** Luncurkan program loyalitas khusus untuk mengubah pembeli satu kali menjadi pelanggan tetap.
""")

st.caption("Copyright © Ahmad Bintang Rafli Maulana 2026")
