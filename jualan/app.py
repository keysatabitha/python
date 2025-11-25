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
    diskon_persen = st.slider("Diskon (%)", min_value=0, max_value=50, value=0, key='diskon_persen')
    diskon_amount = subtotal_semua * (diskon_persen / 100)
    
    total_bersih = subtotal_semua - diskon_amount
    
    st.markdown(f"Diskon: **Rp {diskon_amount:,.0f}** ({diskon_persen}%)")
    st.markdown(f"## Total Tagihan Bersih: **Rp {total_bersih:,.0f}**", unsafe_allow_html=True)
    
with col_action:
    st.markdown("### Aksi Transaksi")
    
    # Input Pembayaran
    pembayaran = st.number_input(
        "Jumlah Uang Dibayar Pelanggan (Rp)", 
        min_value=total_bersih, 
        value=total_bersih if total_bersih > 0 else 0.0, 
        step=1000.0
    )
    
    kembalian = pembayaran - total_bersih
    st.markdown(f"Uang Kembalian: **Rp {kembalian:,.0f}**", unsafe_allow_html=True)

    # Tombol Selesaikan Transaksi
    if st.session_state.cart and pembayaran >= total_bersih:
        if st.button("Selesaikan Transaksi & Cetak Struk 🖨️", key="complete_btn"):
            # Lakukan pencatatan riwayat
            item_list_for_history = [(item['Nama'], item['Kuantitas']) for item in st.session_state.cart]
            add_to_history(item_list_for_history, total_bersih, diskon_amount)
            
            # Tampilkan pesan sukses dan struk sederhana
            st.balloons()
            st.success(f"Transaksi Selesai! Kembalian Rp {kembalian:,.0f}")
            
            # Reset state setelah transaksi selesai
            st.session_state.cart = []
            st.session_state.diskon_persen = 0
            st.session_state.quantities = {k: 0 for k in PRODUCTS.keys()}
            
            # Force rerun agar input kuantitas direset
            st.experimental_rerun() 
            
    elif not st.session_state.cart:
        st.warning("Tambahkan item ke keranjang untuk menyelesaikan transaksi.")
    elif pembayaran < total_bersih:
        st.warning("Jumlah pembayaran kurang dari total tagihan.")
        

# --- Bagian 3: Riwayat Transaksi (Simulasi Database) ---
st.markdown("---")
st.header("3. Riwayat Penjualan Harian")

if not st.session_state.history.empty:
    st.dataframe(st.session_state.history, use_container_width=True)
else:
    st.info("Belum ada transaksi yang tercatat hari ini.")

st.markdown("---")
st.caption("Dibuat dengan Python Streamlit untuk solusi POS sederhana.")
