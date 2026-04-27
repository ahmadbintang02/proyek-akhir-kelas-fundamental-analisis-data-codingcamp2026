import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

# Set Page Config
st.set_page_config(page_title="E-commerce Data Dashboard", layout="wide")

# Helper function untuk memuat data
def load_data():
    # Pastikan nama file sesuai dengan hasil export notebook Anda
    monthly_df = pd.read_csv("dashboard/monthly_revenue_clean.csv")
    city_df = pd.read_csv("dashboard/city_revenue_clean.csv")
    rfm_df = pd.read_csv("dashboard/rfm_clean.csv") 
    
    monthly_df['order_purchase_timestamp'] = pd.to_datetime(monthly_df['order_purchase_timestamp'])
    return monthly_df, city_df, rfm_df

# Memanggil data
monthly_revenue_df, city_revenue_df, rfm_df = load_data()

# --- SIDEBAR ---
with st.sidebar:
    st.title("Proyek Akhir Kelas Fundamental Analisis Data")
    
    min_date = monthly_revenue_df["order_purchase_timestamp"].min()
    max_date = monthly_revenue_df["order_purchase_timestamp"].max()
    
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Filter Data berdasarkan input sidebar
main_df = monthly_revenue_df[
    (monthly_revenue_df["order_purchase_timestamp"] >= pd.to_datetime(start_date)) & 
    (monthly_revenue_df["order_purchase_timestamp"] <= pd.to_datetime(end_date))
]

# --- MAIN PAGE ---
st.title("📊 E-commerce Public Dashboard")

# TEKS PEMBUKA DATASET
st.markdown("""
### **Tentang Dataset**
Dashboard ini menyajikan analisis mendalam dari **E-commerce Public Dataset**. Data ini mencakup informasi riwayat pesanan, detail pembayaran, hingga profil geografis pelanggan. Tujuan utama dari eksplorasi ini adalah untuk memahami tren pertumbuhan pendapatan perusahaan serta mengidentifikasi karakteristik perilaku belanja pelanggan demi mendukung pengambilan keputusan strategis.
""")

st.markdown("---")

# 1. TREN PENDAPATAN BULANAN
st.subheader("Tren Pendapatan Bulanan")
fig, ax = plt.subplots(figsize=(14, 6))

# Menyiapkan Data (Semua data dari awal sampai akhir)
x_months = monthly_revenue_df['order_purchase_timestamp'].dt.strftime('%b %Y')  
y_revenue = monthly_revenue_df['revenue'] / 1_000_000

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

# Mengatur Grid
plt.grid(axis='y', linestyle='--', alpha=0.3)
plt.grid(axis='x', linestyle=':', alpha=0.5)

# Pelabelan
plt.title("Tren Pendapatan Bulanan (Seluruh Periode)", loc="left", fontsize=16, pad=25)
plt.xlabel("Bulan Pembelian", fontsize=12, labelpad=15)
plt.ylabel("Total Pendapatan (Juta BRL)", fontsize=12, labelpad=15)

plt.xticks(rotation=45, ha='right', fontsize=10)

# Menghilangkan distraksi visual (Spines)
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)

ax.set_ylim(bottom=-0.05) 

st.pyplot(fig)

# Analisis Explanatory Pertanyaan 1
st.info("""
**Insight Tren Pendapatan:**
* Pendapatan menunjukkan tren pertumbuhan yang positif dan signifikan. Setelah fase awal yang lambat pada akhir 2016, bisnis mengalami akselerasi sejak awal 2017. 
* Puncak performa tertinggi tercapai pada **November 2017**, di mana pendapatan melampaui **1.2 Juta BRL**, yang mengindikasikan keberhasilan strategi musiman pada periode tersebut.
""")

st.markdown("---")

# 2. KOTA DENGAN PENDAPATAN TERTINGGI
st.subheader("10 Kota dengan Pendapatan Tertinggi")
fig_city, ax_city = plt.subplots(figsize=(12, 7))

sns.barplot(
    x="payment_value", 
    y="customer_city", 
    data=city_revenue_df.head(10), 
    color="#1976D2", 
    ax=ax_city
)

# Labeling yang mendetail untuk menghindari ambiguitas
plt.title("10 Kota dengan Total Transaksi Tertinggi", loc="left", fontsize=14, pad=20)
plt.xlabel("Total Pendapatan (Ribu BRL)", fontsize=10)
plt.ylabel("Nama Kota", fontsize=10)

# Menghilangkan distraksi visual
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)

st.pyplot(fig_city)

# Analisis Explanatory Pertanyaan 2
st.info("""
**Insight Distribusi Geografis:**
* Distribusi pendapatan sangat terkonsentrasi di wilayah metropolitan. Kota **Sao Paulo** merupakan kontributor pendapatan terbesar secara mutlak, disusul oleh Rio de Janeiro. 
* Dominasi ini menunjukkan bahwa basis pelanggan utama berada di pusat ekonomi utama Brasil, sehingga efisiensi operasional masih sangat bergantung pada performa di wilayah tersebut.
""")

st.markdown("---")

# 3. RFM ANALYSIS
st.subheader("Distribusi Segmen Pelanggan (RFM Analysis)")
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

for p in ax_rfm.patches:
    ax_rfm.annotate(f'{int(p.get_height())}', 
                (p.get_x() + p.get_width() / 2., p.get_height()), 
                ha = 'center', va = 'center', 
                xytext = (0, 9), 
                textcoords = 'offset points',
                fontsize=10)

st.pyplot(fig_rfm)

# Analisis Explanatory RFM
st.info("""
**Insight Analisis RFM:**
* Sebagian besar pelanggan berada pada segmen **Low Value Customer**, yang mengindikasikan banyaknya pembeli satu kali (*one-time buyers*). 
* Meskipun jumlahnya sedikit, segmen **Top Customer** memiliki kontribusi nilai transaksi yang masif. Perusahaan disarankan fokus pada program loyalitas untuk meningkatkan frekuensi belanja pada segmen ini.
""")

st.caption("Copyright © Ahmad Bintang Rafli Maulana 2026")
