import streamlit as st

st.title("Program Pengurutan 3 Bilangan")

st.write("Masukkan tiga bilangan, kemudian program akan menampilkan urutan dari yang terkecil ke terbesar.")

# Input
a = st.number_input("Masukkan bilangan pertama:", step=1)
b = st.number_input("Masukkan bilangan kedua:", step=1)
c = st.number_input("Masukkan bilangan ketiga:", step=1)

if st.button("Urutkan"):
    # Proses pengurutan
    sorted_numbers = sorted([a, b, c])
    
    st.success(f"Urutan bilangan dari yang paling kecil: {sorted_numbers[0]}, {sorted_numbers[1]}, {sorted_numbers[2]}")
