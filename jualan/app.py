import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# --- Konfigurasi Produk & Harga ---
# Data produk dalam format: {Nama Produk: Harga Jual}
PRODUCTS = {
    "Tepung Terigu Segitiga Biru (kg)": 12000,
    "Gula Halus (kg)": 14000,
    "Telur Ayam (butir)": 2000,
    "Butter Anchor (200g)": 45000,
    "Cokelat Batangan Collata (250g)": 22000,
    "Ragi Instan Saf Instant (sachet)": 7000,
    "Vanili Bubuk (sachet)": 1500,
    "Loyang Kue Bulat (20cm)": 35000,
    "Spatula Silikon": 18000,
}

# --- Konfigurasi Gaya (CSS) yang Menarik dan Berwarna ---
st.set_page_config(
    page_title="Sistem Kasir Toko Kue",
    layout="wide",
    initial_sidebar_state="expanded"
)

COLOR_PRIMARY = "#FF5733" # Merah-Oranye (Enerjik)
COLOR_SECONDARY = "#33FF57" # Hijau Cerah
COLOR_BACKGROUND = "#F5F5F5" # Abu-abu Pucat
COLOR_ACCENT = "#3366FF" # Biru (Tombol)

st.markdown(f"""
    <style>
    .stApp {{background-color: {COLOR_BACKGROUND};}}
    h1 {{color: {COLOR_PRIMARY}; text-align: center;}}
    .stButton>button {{
        background-color: {COLOR_ACCENT}; 
        color: white;
        border-radius: 10px;
        font-weight: bold;
        padding: 10px 20px;
    }}
    .price-box {{
        background-color: #FFFACD; /* Lemon Chiffon */
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid {COLOR_PRIMARY};
        margin-bottom: 10px;
    }}
    </style>
""", unsafe_allow_html=True)

# --- State Management ---
if 'cart' not in st.session_state:
    st.session_state.cart = []
if 'history' not in st.session_state:
    st.session_state.history = pd.DataFrame(columns=['Tanggal', 'Item', 'Total Bersih', 'Diskon'])

def add_to_history(cart_items, final_total, discount_amount):
    """Menambahkan transaksi ke riwayat."""
    item_summary = ", ".join([f"{name} ({qty})" for name, qty in cart_items])
    new_row = pd.DataFrame([{
        'Tanggal': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'Item': item_summary,
        'Total Bersih': f"Rp {final_total:,.0f}",
        'Diskon': f"Rp {discount_amount:,.0f}"
    }])
    st.session_state.history = pd.concat([st.session_state.history, new_row], ignore_index=True)

def reset_transaction():
    """Mengatur ulang keranjang belanja untuk transaksi baru."""
    st.session_state.cart = []
    st.session_state.diskon_persen = 0
    st.success("Transaksi baru dimulai!")

# --- Judul Aplikasi ---
st.title("🍰 Sistem Penjualan Toko Bahan Kue 🛒")
st.markdown("---")

# --- Bagian 1: Input Penjualan (Keranjang) ---
st.header("1. Masukkan Item Penjualan")
st.markdown("Pilih kuantitas produk yang dibeli pelanggan.")

col_produk, col_keranjang = st.columns(2)

with col_produk:
    st.subheader("Daftar Produk")
    
    # Input Kuantitas Produk
    st.session_state.quantities = {}
    cart_list = []
    
    for product_name, price in PRODUCTS.items():
        # Gunakan key unik untuk setiap input
        key_input = f"qty_{product_name.replace(' ', '_').replace('(', '').replace(')', '')}"
        
        col_name, col_price, col_qty = st.columns([3, 2, 1])
        
        with col_name:
            st.markdown(f"**{product_name}**")
        with col_price:
            st.markdown(f"Rp {price:,.0f}")
        with col_qty:
            qty = st.number_input(
                "Kuantitas", 
                min_value=0, 
                max_value=100, 
                value=0, 
                step=1, 
                key=key_input,
                label_visibility="collapsed"
            )
            
        st.session_state.quantities[product_name] = qty
        if qty > 0:
            cart_list.append({
                "Nama": product_name,
                "Harga": price,
                "Kuantitas": qty,
                "Subtotal": price * qty
            })

    # Update Cart State
    st.session_state.cart = cart_list

with col_keranjang:
    st.subheader("Keranjang Belanja Saat Ini")
    if st.session_state.cart:
        df_cart = pd.DataFrame(st.session_state.cart)
        # Hapus kolom Harga (sudah ada di subtotal)
        df_display = df_cart[['Nama', 'Kuantitas', 'Subtotal']]
        df_display['Subtotal'] = df_display['Subtotal'].apply(lambda x: f"Rp {x:,.0f}")
        
        st.dataframe(df_display, hide_index=True, use_container_width=True)
    else:
        st.info("Keranjang kosong. Silakan masukkan kuantitas produk di sebelah kiri.")

# --- Bagian 2: Kalkulasi & Pembayaran ---
st.markdown("---")
st.header("2. Ringkasan & Pembayaran")

# Perhitungan Dasar
subtotal_semua = sum(item['Subtotal'] for item in st.session_state.cart)

col_summary, col_action = st.columns([1, 1])

with col_summary:
    st.markdown(f'<div class="price-box">Total Subtotal (Sebelum Diskon): </div>', unsafe_allow_html=True)
    st.markdown(f"## **Rp {subtotal_semua:,.0f}**")
    
    # Input Diskon
    diskon_persen = st.slider("Diskon (%)
