import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# --- Fungsi Transformasi Geometri ---

def translate(x, y, tx, ty):
    """Translasi: (x + tx, y + ty)"""
    return x + tx, y + ty

def rotate(x, y, angle_deg, cx=0, cy=0):
    """Rotasi: Sudut dalam derajat, berpusat di (cx, cy)"""
    angle_rad = np.deg2rad(angle_deg)
    # Pindahkan ke pusat (0,0)
    x_prime = x - cx
    y_prime = y - cy
    # Rotasi
    x_rotated = x_prime * np.cos(angle_rad) - y_prime * np.sin(angle_rad)
    y_rotated = x_prime * np.sin(angle_rad) + y_prime * np.cos(angle_rad)
    # Pindahkan kembali
    return x_rotated + cx, y_rotated + cy

def reflect(x, y, axis):
    """Refleksi: Terhadap sumbu X, Y, garis y=x, atau garis y=-x"""
    if axis == 'Sumbu X (y=0)':
        return x, -y
    elif axis == 'Sumbu Y (x=0)':
        return -x, y
    elif axis == 'Garis y = x':
        return y, x
    elif axis == 'Garis y = -x':
        return -y, -x
    return x, y # Default

def dilate(x, y, kx, ky, cx=0, cy=0):
    """Dilatasi: Faktor skala kx dan ky, berpusat di (cx, cy)"""
    # Pindahkan ke pusat (0,0)
    x_prime = x - cx
    y_prime = y - cy
    # Dilatasi
    x_dilated = x_prime * kx
    y_dilated = y_prime * ky
    # Pindahkan kembali
    return x_dilated + cx, y_dilated + cy

# --- Setup Aplikasi Streamlit ---

st.set_page_config(
    page_title="Virtual Lab Transformasi Geometri",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🔬 Virtual Lab Transformasi Geometri Interaktif")
st.markdown("Eksplorasi Rotasi, Refleksi, Dilatasi, dan Translasi secara visual.")

col1, col2 = st.columns([1, 2])

with col1:
    st.header("⚙️ Pengaturan")

    # 1. Input Objek Awal
    st.subheader("1. Objek Awal (Poligon/Titik)")
    st.info("Masukkan koordinat titik (x, y) dipisahkan koma, contoh: 1,1; 3,1; 3,4")
    
    input_coords = st.text_input(
        "Koordinat Titik (format: x1,y1; x2,y2; ...)", 
        "1,1; 3,1; 2,3; 1,1"
    )
    
    try:
        # Parsing input koordinat
        coords = []
        for pair in input_coords.split(';'):
            x, y = map(float, pair.strip().split(','))
            coords.append((x, y))
        
        X_orig = np.array([c[0] for c in coords])
        Y_orig = np.array([c[1] for c in coords])
        is_valid_input = True
        
    except:
        st.error("Format koordinat tidak valid. Pastikan formatnya 'x1,y1; x2,y2; ...'")
        is_valid_input = False
        X_orig, Y_orig = np.array([0]), np.array([0])


    # 2. Pilihan Transformasi
    st.subheader("2. Pilih Transformasi")
    transform_type = st.selectbox(
        "Jenis Transformasi",
        ["Translasi", "Rotasi", "Refleksi", "Dilatasi"]
    )
    
    # 3. Input Parameter Transformasi
    st.subheader("3. Parameter Transformasi")
    X_trans = X_orig
    Y_trans = Y_orig

    if transform_type == "Translasi":
        tx = st.slider("Vektor Translasi X ($t_x$)", -10.0, 10.0, 3.0, 0.5)
        ty = st.slider("Vektor Translasi Y ($t_y$)", -10.0, 10.0, 2.0, 0.5)
        X_trans, Y_trans = translate(X_orig, Y_orig, tx, ty)

    elif transform_type == "Rotasi":
        angle = st.slider("Sudut Rotasi (Derajat)", -360, 360, 90)
        cx = st.number_input("Pusat Rotasi X ($c_x$)", value=0.0)
        cy = st.number_input("Pusat Rotasi Y ($c_y$)", value=0.0)
        X_trans, Y_trans = rotate(X_orig, Y_orig, angle, cx, cy)
        st.caption(f"Rotasi sebesar **{angle}°** berpusat di **({cx}, {cy})**")

    elif transform_type == "Refleksi":
        axis = st.selectbox(
            "Garis Cermin",
            ['Sumbu X (y=0)', 'Sumbu Y (x=0)', 'Garis y = x', 'Garis y = -x']
        )
        X_trans, Y_trans = reflect(X_orig, Y_orig, axis)
        st.caption(f"Refleksi terhadap **{axis}**")

    elif transform_type == "Dilatasi":
        kx = st.slider("Faktor Skala X ($k_x$)", 0.1, 5.0, 2.0, 0.1)
        ky = st.slider("Faktor Skala Y ($k_y$)", 0.1, 5.0, 2.0, 0.1)
        cx = st.number_input("Pusat Dilatasi X ($c_x$)", value=0.0)
        cy = st.number_input("Pusat Dilatasi Y ($c_y$)", value=0.0)
        X_trans, Y_trans = dilate(X_orig, Y_orig, kx, ky, cx, cy)
        st.caption(f"Dilatasi dengan faktor $k_x={kx}, k_y={ky}$ berpusat di **({cx}, {cy})**")


with col2:
    st.header("📈 Visualisasi Hasil")
    
    if is_valid_input:
        
        # Penentuan batas sumbu X dan Y
        all_x = np.concatenate([X_orig, X_trans])
        all_y = np.concatenate([Y_orig, Y_trans])
        
        x_min, x_max = all_x.min() - 1, all_x.max() + 1
        y_min, y_max = all_y.min() - 1, all_y.max() + 1
        
        # Pastikan batas minimum dan maksimum mencakup titik (0,0)
        x_min = min(x_min, -1)
        x_max = max(x_max, 1)
        y_min = min(y_min, -1)
        y_max = max(y_max, 1)

        # Buat Plot
        fig, ax = plt.subplots(figsize=(8, 8))
        
        # Gambar objek awal
        ax.plot(X_orig, Y_orig, 'b--', label='Objek Awal (P)')
        ax.fill(X_orig, Y_orig, 'lightblue', alpha=0.5)

        # Gambar objek hasil transformasi
        ax.plot(X_trans, Y_trans, 'r-', label='Hasil Transformasi (P\')')
        ax.fill(X_trans, Y_trans, 'salmon', alpha=0.7)

        # Label koordinat titik awal
        for i in range(len(X_orig) - 1): # Abaikan titik terakhir jika objek ditutup
            ax.text(X_orig[i], Y_orig[i], f'P{i+1}({X_orig[i]:.1f},{Y_orig[i]:.1f})', color='blue', fontsize=8, ha='right')
        
        # Label koordinat titik hasil
        for i in range(len(X_trans) - 1):
             ax.text(X_trans[i], Y_trans[i], f"P'{i+1}({X_trans[i]:.1f},{Y_trans[i]:.1f})", color='red', fontsize=8, ha='left')


        # Pengaturan Grid dan Axis
        ax.axhline(0, color='gray', linewidth=0.5)
        ax.axvline(0, color='gray', linewidth=0.5)
        ax.grid(True, linestyle='--', alpha=0.6)
        ax.set_xlabel("Sumbu X")
        ax.set_ylabel("Sumbu Y")
        ax.set_title(f"Visualisasi {transform_type}")
        
        # Atur batas sumbu
        ax.set_xlim(x_min, x_max)
        ax.set_ylim(y_min, y_max)
        ax.set_aspect('equal', adjustable='box') # Penting agar skala X dan Y sama
        
        ax.legend()
        st.pyplot(fig)
        
        # Tampilkan Hasil Perhitungan dalam bentuk tabel
        st.subheader("Tabel Koordinat")
        data = {
            'Titik Awal ($P$)': [f'({X_orig[i]:.2f}, {Y_orig[i]:.2f})' for i in range(len(X_orig)-1)],
            'Titik Hasil ($P^\prime$)': [f'({X_trans[i]:.2f}, {Y_trans[i]:.2f})' for i in range(len(X_trans)-1)]
        }
        st.table(data)
        
        # Penjelasan Konsep Singkat
        st.subheader("💡 Konsep Dasar")
        if transform_type == "Translasi":
            st.markdown("Translasi adalah pergeseran setiap titik objek atau bentuk dengan jarak dan arah yang sama. Ditentukan oleh **Vektor Translasi** $(t_x, t_y)$.")
        elif transform_type == "Rotasi":
            st.markdown("Rotasi adalah perputaran objek pada titik pusat tertentu dengan sudut tertentu. Rotasi mempertahankan bentuk dan ukuran objek.")
        elif transform_type == "Refleksi":
            st.markdown("Refleksi adalah pencerminan objek. Setiap titik objek berjarak sama dari **Garis Cermin**.")
        elif transform_type == "Dilatasi":
            st.markdown("Dilatasi adalah perubahan ukuran objek (memperbesar atau memperkecil) tanpa mengubah bentuknya. Ditentukan oleh **Faktor Skala** ($k$) dan **Pusat Dilatasi**.")
        
    else:
         st.warning("Mohon perbaiki format koordinat di kolom kiri untuk menampilkan visualisasi.")
