# E-Commerce Data Analysis Dashboard ✨

## Deskripsi
Dashboard ini dikembangkan sebagai bagian dari Proyek Akhir Analisis Data pada program Dicoding. Dashboard ini memberikan wawasan mendalam mengenai tren pendapatan bulanan, distribusi geografis pelanggan, dan segmentasi pelanggan menggunakan analisis RFM pada E-commerce Public Dataset.

## Setup Environment - Anaconda
conda create --name main-ds python=3.9
conda activate main-ds
pip install -r requirements.txt

## Setup Environment - Shell/Terminal
mkdir proyek_analisis_data
cd proyek_analisis_data
pipenv install
pipenv shell
pip install -r requirements.txt

## Persiapan Data (File CSV)
Pastikan file berikut berada di folder yang sama dengan `dashboard.py`:
- `monthly_revenue_clean.csv`
- `city_revenue_clean.csv`
- `rfm_clean.csv`

## Run Streamlit App
streamlit run dashboard.py

## Struktur Proyek
- `/dashboard`: Berisi file dashboard utama (dashboard.py) dan dataset hasil pembersihan.
- `/data`: Berisi raw data.
- `notebook.ipynb`: File analisis data lengkap mulai dari Wrangling hingga Conclusion.
- `README.md`: Dokumentasi cara menjalankan proyek.
- `requirements.txt`: Daftar library yang dibutuhkan.
- `url.txt`: Berisi tautan untuk dashboard streamlit cloud.
