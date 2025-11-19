import streamlit as st

def hitung_imt(berat_kg, tinggi_m):
    """Menghitung Indeks Massa Tubuh."""
    return berat_kg / (tinggi_m ** 2)

st.title("Aplikasi Penghitung Indeks Massa Tubuh (IMT)")
st.write("Masukkan berat dan tinggi badan Anda untuk menghitung IMT.")

# Input berat dan tinggi
berat = st.number_input("Masukkan berat badan (kg):", min_value=1.0, step=0.1)
tinggi = st.number_input("Masukkan tinggi badan (meter):", min_value=0.3, step=0.01)

if st.button("Hitung IMT"):
    imt = hitung_imt(berat, tinggi)
    st.write(f"### Nilai IMT Anda: **{imt:.2f}**")

    # Kategori IMT
    if imt < 18.5:
        kategori = "Kurus / Kekurangan berat badan"
        st.warning(kategori)
    elif 18.5 <= imt < 25.0:
        kategori = "Normal / Ideal"
        st.success(kategori)
    elif 25.0 <= imt < 30.0:
        kategori = "Kelebihan berat badan"
        st.info(kategori)
    else:
