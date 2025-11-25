import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import math

# --- Konfigurasi Gaya & Header ---
st.set_page_config(
    page_title="Virtual Lab Lingkaran",
    layout="wide",
    initial_sidebar_state="expanded"
)

COLOR_PRIMARY = "#20B2AA"  # Light Sea Green
COLOR_ACCENT = "#FFD700"   # Gold
COLOR_TEXT = "#333333"

st.markdown(f"""
    <style>
    h1 {{color: {COLOR_PRIMARY}; text-align: center;}}
    .metric-box {{
        background-color: #F0F8FF; /* Alice Blue */
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid {COLOR_ACCENT};
        margin-bottom: 10px;
    }}
    .stNumberInput, .stSlider {{
        font-size: 18px;
    }}
    </style>
""", unsafe_allow_html=True)

st.title("⭕ Virtual Lab: Properti Lingkaran")
st.markdown("Eksplorasi hubungan antara Jari-jari, Diameter, Keliling, Luas, dan Sudut.")

# --- Bagian 1: Input dan Pengaturan ---
st.sidebar.header("⚙️ Pengaturan Lingkaran")
st.sidebar.markdown("Pilih input utama Anda:")

input_mode = st.sidebar.radio(
    "Pilih Input Utama",
    ('Jari-jari (r)', 'Diameter (d)')
)

# Input Jari-jari atau Diameter
if input_mode == 'Jari-jari (r)':
    r = st.sidebar.slider("Masukkan Jari-jari (r)", min_value=1.0, max_value=10.0, value=3.0, step=0.5)
    d = 2 * r
else:
    d = st.sidebar.slider("Masukkan Diameter (d)", min_value=2.0, max_value=20.0, value=6.0, step=1.0)
    r = d / 2

# Input Sudut untuk Busur dan Juring
st.sidebar.markdown("---")
st.sidebar.subheader("Sudut Pusat")
angle_deg = st.sidebar.slider(
    "Masukkan Sudut Pusat (θ) dalam Derajat", 
    min_value=0, 
    max_value=360, 
    value=90, 
    step=5
)

angle_rad = math.radians(angle_deg)
phi_approx = 3.1415926535

# --- Bagian 2: Perhitungan Metrik ---
Keliling = 2 * phi_approx * r
Luas = phi_approx * (r ** 2)
Luas_Juring = (angle_deg / 360) * Luas
Panjang_Busur = (angle_deg / 360) * Keliling

# --- Tampilan Hasil di Kolom Utama ---
col_calc, col_viz = st.columns([1, 2])

with col_calc:
    st.header("📏 Hasil Perhitungan")
    st.markdown(f"**Menggunakan π ≈ {phi_approx}**")

    # Tampilkan Jari-jari dan Diameter
    st.markdown(f'<div class="metric-box"><h4>Jari-jari (r):</h4> <h3>{r:.2f} satuan</h3></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-box"><h4>Diameter (d):</h4> <h3>{d:.2f} satuan</h3></div>', unsafe_allow_html=True)
    
    st.subheader("Ukuran Utama")
    st.markdown(f'<div class="metric-box"><h4>Keliling (K = 2πr):</h4> <h3>{Keliling:.2f} satuan</h3></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-box"><h4>Luas (L = πr²):</h4> <h3>{Luas:.2f} satuan²</h3></div>', unsafe_allow_html=True)
    
    st.subheader(f"Ukuran Sudut (θ = {angle_deg}°)")
    st.markdown(f'<div class="metric-box"><h4>Luas Juring:</h4> <h3>{Luas_Juring:.2f} satuan²</h3></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-box"><h4>Panjang Busur:</h4> <h3>{Panjang_Busur:.2f} satuan</h3></div>', unsafe_allow_html=True)


with col_viz:
    st.header("🖼️ Visualisasi Lingkaran")
    
    # Buat Plot Matplotlib
    fig, ax = plt.subplots(figsize=(7, 7))
    
    # Atur batas plot agar simetris
    limit = r + 1.5
    ax.set_xlim(-limit, limit)
    ax.set_ylim(-limit, limit)
    ax.set_aspect('equal', adjustable='box')
    
    # Gambar Lingkaran Penuh
    circle = plt.Circle((0, 0), r, color=COLOR_PRIMARY, fill=False, linewidth=2, label=f'r = {r}')
    ax.add_artist(circle)
    
    # Titik Pusat
    ax.plot(0, 0, 'o', color='black')
    ax.text(0.1, 0.1, 'Pusat (0,0)', fontsize=10)
    
    # Gambar Jari-jari (sebagai garis r)
    ax.plot([0, r], [0, 0], 'r--', linewidth=1)
    ax.text(r / 2, 0.2, f'r = {r:.1f}', color='red', fontsize=10)
    
    # Gambar Diameter
    ax.plot([-r, r], [0, 0], 'b-', alpha=0.5, linewidth=3, label=f'd = {d}')

    # --- Visualisasi Sudut (Juring & Busur) ---
    if angle_deg > 0:
        
        # Gambar Juring (Sektor)
        theta_start = 0
        theta_end = angle_rad
        
        # Buat Path untuk mengisi Juring
        t = np.linspace(theta_start, theta_end, 50)
        x_sector = r * np.cos(t)
        y_sector = r * np.sin(t)
        
        sector_path = np.array([(0, 0)] + list(zip(x_sector, y_sector)) + [(0, 0)])
        ax.fill(sector_path[:, 0], sector_path[:, 1], color=COLOR_ACCENT, alpha=0.4, label='Juring')

        # Label Sudut
        ax.text(r * 0.45 * np.cos(angle_rad / 2), r * 0.45 * np.sin(angle_rad / 2), 
                f'{angle_deg}°', color='black', fontsize=12, weight='bold')

        # Gambar Busur (arc)
        ax.plot(x_sector, y_sector, color=COLOR_ACCENT, linewidth=3, label='Busur')

        # Gambar Sisi Akhir Sudut
        ax.plot([0, r * math.cos(angle_rad)], [0, r * math.sin(angle_rad)], 
                color=COLOR_ACCENT, linestyle='--', linewidth=1)

    # Label Axis dan Title
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(f"Visualisasi Lingkaran (r={r:.1f}, θ={angle_deg}°)", fontsize=14)
    ax.legend(loc='upper right')

    st.pyplot(fig)
    
    st.caption("""
    * Area berwarna Gold adalah **Juring**.
    * Garis tebal pada Keliling adalah **Busur** (panjang busur).
    * Garis putus-putus merah adalah **Jari-jari (r)**.
    * Garis tebal biru adalah **Diameter (d)**.
    """)
