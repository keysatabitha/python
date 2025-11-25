import streamlit as st

# --- Konfigurasi Gaya (CSS) yang Menarik dan Berwarna ---
st.set_page_config(
    page_title="Pesan Motivasi Josjis",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Definisi Warna Cerah
COLOR_BG = "#FFFFE0"  # Light Yellow / Lemon
COLOR_PRIMARY = "#FF4500" # Orange Red (Untuk Teks Utama)
COLOR_ACCENT = "#1E90FF"  # Dodger Blue (Untuk Dekorasi)

# Gunakan Markdown dengan HTML/CSS untuk styling kustom
st.markdown(f"""
    <style>
    .stApp {{background-color: {COLOR_BG};}}
    
    .motivation-box {{
        background-color: #FFFFFF; /* Kotak Putih untuk kontras */
        padding: 40px;
        border-radius: 20px;
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
        text-align: center;
        border: 5px dashed {COLOR_ACCENT}; /* Border menarik */
        margin-top: 50px;
    }}
    
    .main-text {{
        font-family: 'Arial Black', sans-serif; /* Font tebal dan mudah dibaca */
        font-size: 50px;
        color: {COLOR_PRIMARY};
        text-shadow: 3px 3px 5px rgba(0, 0, 0, 0.3);
        line-height: 1.2;
    }}
    
    .decoration-icon {{
        font-size: 80px;
        color: {COLOR_ACCENT};
        margin: 0 20px;
        animation: pulse 1s infinite alternate; /* Efek animasi */
    }}

    @keyframes pulse {{
        from {{transform: scale(1);}}
        to {{transform: scale(1.1);}}
    }}
    </style>
""", unsafe_allow_html=True)

# --- Konten Utama Aplikasi ---

# Struktur Konten dalam kotak yang menarik
html_content = f"""
<div class="motivation-box">
    
    <div class="decoration-line">
        <span class="decoration-icon">🌟</span>
        <span class="decoration-icon">🚀</span>
    </div>
    
    <div class="main-text">
        Semangat terus josjis<br>
        JANGAN KASI KENDOR!
    </div>
    
    <div class="decoration-line">
        <span class="decoration-icon">💪</span>
        <span class="decoration-icon">🔥</span>
    </div>
    
</div>
"""

st.markdown(html_content, unsafe_allow_html=True)

# Footer sederhana
st.markdown("---")
st.markdown("Pesan ini dideploy menggunakan Streamlit.")
