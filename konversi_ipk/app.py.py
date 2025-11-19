import streamlit as st

st.title(“Penentuan Nilai Huruf”)

nilai = st.number_input(“Masukkan nilai Anda:”, min_value=0.0,
max_value=100.0, step=0.1)

if st.button(“Cek Nilai”): if nilai > 100 or nilai < 0: st.error(“Nilai
Anda tidak valid (di luar rentang 0-100)”) elif nilai >= 85:
st.success(“Nilai Anda A”) elif nilai >= 70: st.info(“Nilai Anda B”)
elif nilai >= 55: st.warning(“Nilai Anda C”) elif nilai >= 40:
st.warning(“Nilai Anda D”) else: st.error(“Nilai Anda E”)
