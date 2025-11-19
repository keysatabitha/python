import streamlit as st

def hitung_pangkat(bilangan):
    """Menghitung kuadrat dan kubik dari sebuah bilangan."""
    kuadrat = bilangan ** 2
    kubik = bilangan ** 3
    return kuadrat, kubik

st.title("Aplikasi Penghitung Kuadrat dan Kubik")
st.write("Masukkan sebuah bilangan untuk menghitung pangkat 2 dan pangkat 3.")

# Input bilangan
angka = st.number_input("Masukkan sebuah bilangan:", step=1.0)

if st.button("Hitung Pangkat"):
    kuadrat, kubik = hitung_pangkat(angka)

    st.subheader(f"Hasil Pangkat dari {angka}")
    st.write(f"**Kuadrat (Pangkat 2): {kuadrat:.2f}**")
    st.write(f"**Kubik (Pangkat 3): {kubik:.2f}**")
