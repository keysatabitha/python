import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from sympy import symbols, sympify, latex, diff

# --- Konfigurasi Gaya & Header ---
st.set_page_config(
    page_title="Virtual Lab Fungsi Ganjil & Genap",
    layout="wide",
    initial_sidebar_state="expanded"
)

COLOR_PRIMARY = "#FF4500"  # Orange Red
COLOR_EVEN = "#1E90FF"     # Dodger Blue
COLOR_ODD = "#32CD32"      # Lime Green
COLOR_TEXT = "#333333"

st.markdown(f"""
    <style>
    h1 {{color: {COLOR_PRIMARY}; text-align: center;}}
    .subheader {{color: {COLOR_TEXT};}}
    .even-box {{background-color: #E0FFFF; border: 3px solid {COLOR_EVEN}; padding: 10px; border-radius: 10px;}}
    .odd-box {{background-color: #F0FFF0; border: 3px solid {COLOR_ODD}; padding: 10px; border-radius: 10px;}}
    </style>
""", unsafe_allow_html=True)

st.title("🔬 Virtual Lab: Fungsi Ganjil & Fungsi Genap")
st.markdown("Eksplorasi Simetri Fungsi secara Aljabar dan Grafis.")

# --- Setup Simbol Variabel ---
x = symbols('x')

# --- Fungsi Inti ---

def classify_function(f_expr, x):
    """Mengklasifikasikan fungsi berdasarkan definisi aljabar."""
    try:
        f_neg_x = f_expr.subs(x, -x)
        neg_f_x = -f_expr

        is_even = f_neg_x.equals(f_expr)
        is_odd = f_neg_x.equals(neg_f_x)

        if is_even:
            return "Genap (Even)", f_neg_x, neg_f_x
        elif is_odd:
            return "Ganjil (Odd)", f_neg_x, neg_f_x
        else:
            return "Bukan Ganjil dan Bukan Genap (Neither)", f_neg_x, neg_f_x
    except Exception as e:
        return f"Error: {e}", None, None

def plot_function(f_expr, result_type):
    """Membuat plot interaktif menggunakan Matplotlib."""
    try:
        # Konversi ekspresi sympy ke fungsi numpy yang dapat diplot
        f_numpy = lambda val: np.array([f_expr.subs(x, float(i)) for i in val], dtype=float)
        
        # Batas plot
        x_vals = np.linspace(-5, 5, 400)
        y_vals = f_numpy(x_vals)
        
        # Ambil hanya nilai yang valid (hindari error log/sqrt)
        valid_indices = np.isfinite(y_vals)
        x_vals = x_vals[valid_indices]
        y_vals = y_vals[valid_indices]

        fig, ax = plt.subplots(figsize=(8, 6))
        
        # Plot fungsi utama
        ax.plot(x_vals, y_vals, label=f'$f(x) = {latex(f_expr)}$', color=COLOR_PRIMARY, linewidth=2)
        
        # Penjelasan Simetri
        if result_type == "Genap (Even)":
            ax.axvline(0, color=COLOR_EVEN, linestyle='--', label='Simetri terhadap Sumbu Y')
            ax.text(0.1, ax.get_ylim()[1] * 0.9, "Simetri Y", color=COLOR_EVEN, fontsize=10)
        elif result_type == "Ganjil (Odd)":
            ax.axvline(0, color=COLOR_ODD, linestyle='--', label='Simetri terhadap Titik Asal')
            ax.axhline(0, color=COLOR_ODD, linestyle='--')
            ax.plot(0, 0, 'o', color=COLOR_ODD, label='Titik Asal')
            ax.text(0.1, ax.get_ylim()[1] * 0.9, "Simetri Asal", color=COLOR_ODD, fontsize=10)
        
        # Pengaturan Grid dan Axis
        ax.axhline(0, color='gray', linewidth=0.5)
        ax.axvline(0, color='gray', linewidth=0.5)
        ax.grid(True, linestyle=':', alpha=0.7)
        ax.set_xlabel("x")
        ax.set_ylabel("f(x)")
        ax.set_title(f"Grafik Fungsi: {result_type}", fontsize=14)
        ax.legend()
        ax.set_ylim(np.nanmin(y_vals) - 1, np.nanmax(y_vals) + 1)
        ax.set_xlim(-5, 5)
        
        return fig
        
    except Exception as e:
        st.error(f"Gagal memplot fungsi. Pastikan fungsi valid. Error: {e}")
        return None

# --- UI Layout ---
col_input, col_result = st.columns([1, 2])

with col_input:
    st.subheader("1. Masukkan Fungsi f(x)")
    
    st.info("Gunakan format Python/SymPy. Contoh: x**2, sin(x), x**3 - x, abs(x)")
    
    # Input Teks Fungsi
    f_input = st.text_input(
        "f(x) =", 
        "x**3 - x", # Contoh fungsi ganjil
        key="function_input"
    )
    
    # Tombol Analisis
    if st.button("Analisis Fungsi Sekarang 🚀"):
        st.session_state.run_analysis = True
    
    # Contoh Fungsi Bawaan
    st.markdown("---")
    st.subheader("Contoh Cepat")
    if st.button("Contoh: Fungsi Genap (x² + 4)"):
        st.session_state.function_input = "x**2 + 4"
        st.session_state.run_analysis = True
        st.experimental_rerun()
        
    if st.button("Contoh: Fungsi Ganjil (x³ + 2x)"):
        st.session_state.function_input = "x**3 + 2*x"
        st.session_state.run_analysis = True
        st.experimental_rerun()
        
    if st.button("Contoh: Bukan Keduanya (x² + x)"):
        st.session_state.function_input = "x**2 + x"
        st.session_state.run_analysis = True
        st.experimental_rerun()

# --- Area Hasil dan Visualisasi ---
with col_result:
    if st.session_state.get('run_analysis', False) and f_input:
        try:
            # 1. Parsing Fungsi
            f_expr = sympify(f_input)
            
            # 2. Klasifikasi Aljabar
            result_type, f_neg_x, neg_f_x = classify_function(f_expr, x)
            
            st.header("2. Hasil Analisis")
            
            # Tampilkan Klasifikasi
            if result_type.startswith("Genap"):
                st.markdown(f'<div class="even-box"><h3>✅ KLASIFIKASI: FUNGSI GENAP ({result_type})</h3></div>', unsafe_allow_html=True)
            elif result_type.startswith("Ganjil"):
                st.markdown(f'<div class="odd-box"><h3>✅ KLASIFIKASI: FUNGSI GANJIL ({result_type})</h3></div>', unsafe_allow_html=True)
            else:
                 st.error(f"❌ KLASIFIKASI: {result_type}")

            st.markdown("---")
            
            # 3. Analisis Aljabar
            st.subheader("3. Perbandingan Aljabar")
            
            col_a, col_b = st.columns(2)
            
            with col_a:
                st.markdown(r"#### Hitung $f(-x)$")
                st.latex(f"f(-x) = {latex(f_neg_x)}")
                
            with col_b:
                st.markdown(r"#### Hitung $-f(x)$")
                st.latex(f"-f(x) = {latex(neg_f_x)}")

            st.markdown("#### Kesimpulan Aljabar:")
            if result_type.startswith("Genap"):
                st.success(r"**Fungsi Genap** karena $f(-x) = f(x)$")
            elif result_type.startswith("Ganjil"):
                st.success(r"**Fungsi Ganjil** karena $f(-x) = -f(x)$")
            else:
                st.warning(r"**Bukan Keduanya** karena $f(-x) \neq f(x)$ dan $f(-x) \neq -f(x)$")
            
            st.markdown("---")
            
            # 4. Visualisasi Grafik
            st.subheader("4. Visualisasi Grafik & Simetri")
            fig = plot_function(f_expr, result_type)
            if fig:
                st.pyplot(fig)
            
            st.caption("""
            * **Fungsi Genap:** Grafik simetri terhadap sumbu Y (seperti cermin).
            * **Fungsi Ganjil:** Grafik simetri terhadap titik asal (diputar 180° di sekitar titik (0,0)).
            """)
            
            
        except Exception as e:
            st.error(f"Input fungsi tidak valid. Pastikan Anda menggunakan sintaks yang benar (misalnya: x**2, sin(x)). Error: {e}")
            
    else:
        st.info("Masukkan fungsi di kolom kiri dan tekan tombol Analisis untuk memulai!")
