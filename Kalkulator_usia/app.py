import streamlit as st

def hitung_usia(tahun_lahir, tahun_sekarang=2025):
    """Menghitung usia berdasarkan tahun lahir."""
    return tahun_sekarang - tahun_lahir

st.title("Aplikasi Penghitung Usia")
st.write("Masukkan tahun lahir Anda untuk menghitung usia pada tahun 2025.")

# Input tahun lahir
tahun_lahir = st.number_input("Masukkan Tahun Lahir:", min_value=1900, max_value=2025, step=1)

if st.button("Hitung Usia"):
    usia = hitung_usia(tahun_lahir)
    st.success(f"Jika Anda lahir tahun {tahun_lahir}, maka pada tahun 2025 usia Anda adalah {usia} tahun.")
