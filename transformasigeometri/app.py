"""
Virtual Lab: Transformasi Geometri (Rotasi, Refleksi, Dilatasi, Translasi)
File: virtual_lab_transformasi_geometri_app.py

Deskripsi singkat:
Aplikasi interaktif menggunakan Streamlit untuk memvisualisasikan transformasi geometri
pada poligon (segitiga, persegi, pentagon, dan custom). Pengguna dapat memilih dan
menggabungkan transformasi (translasi, rotasi, refleksi, dilatasi), melihat matriks
transformasi, langkah per langkah, dan mengunduh hasil gambar.

Cara pakai lokal:
1. Buat virtual environment (opsional) dan install requirements.txt
   python -m venv venv
   source venv/bin/activate  # mac/linux
   venv\Scripts\activate     # windows
   pip install -r requirements.txt
2. Jalankan:
   streamlit run virtual_lab_transformasi_geometri_app.py

Cara deploy via GitHub + Streamlit Cloud (ringkasan):
1. Buat repository baru di GitHub.
2. Tambahkan file ini (virtual_lab_transformasi_geometri_app.py) dan requirements.txt ke repo.
3. Commit & push: git add . && git commit -m "add virtual lab" && git push origin main
4. Buka https://share.streamlit.io, login, klik 'New app' -> pilih repo dan branch -> deploy.

requirements.txt (minimal):
streamlit
numpy
matplotlib
pandas

Catatan: file ini ditulis agar mudah dimengerti dan dimodifikasi oleh pengajar atau siswa.

--- KODE APLIKASI ---
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import io
from typing import Tuple

st.set_page_config(page_title="Virtual Lab - Transformasi Geometri", layout="wide")

# ----------------------------- Utilities -----------------------------

def polygon_points(sides: int, radius: float = 1.0, rotation: float = 0.0) -> np.ndarray:
    """Generate polygon vertex coordinates centered at origin."""
    angles = np.linspace(0, 2 * np.pi, sides, endpoint=False) + np.deg2rad(rotation)
    x = radius * np.cos(angles)
    y = radius * np.sin(angles)
    return np.vstack([x, y]).T


def centroid(points: np.ndarray) -> np.ndarray:
    return np.mean(points, axis=0)


def translate(points: np.ndarray, tx: float, ty: float) -> Tuple[np.ndarray, np.ndarray]:
    T = np.array([[1, 0, tx], [0, 1, ty], [0, 0, 1]])
    hom = np.hstack([points, np.ones((points.shape[0], 1))])
    new = (T @ hom.T).T[:, :2]
    return new, T


def rotate(points: np.ndarray, angle_deg: float, about: np.ndarray = None) -> Tuple[np.ndarray, np.ndarray]:
    theta = np.deg2rad(angle_deg)
    R = np.array([[np.cos(theta), -np.sin(theta), 0], [np.sin(theta), np.cos(theta), 0], [0, 0, 1]])
    if about is None:
        hom = np.hstack([points, np.ones((points.shape[0], 1))])
        new = (R @ hom.T).T[:, :2]
        return new, R
    else:
        # translate to origin, rotate, translate back
        tx, ty = about
        T1 = np.array([[1, 0, -tx], [0, 1, -ty], [0, 0, 1]])
        T2 = np.array([[1, 0, tx], [0, 1, ty], [0, 0, 1]])
        M = T2 @ R @ T1
        hom = np.hstack([points, np.ones((points.shape[0], 1))])
        new = (M @ hom.T).T[:, :2]
        return new, M


def dilate(points: np.ndarray, scale: float, about: np.ndarray = None) -> Tuple[np.ndarray, np.ndarray]:
    S = np.array([[scale, 0, 0], [0, scale, 0], [0, 0, 1]])
    if about is None:
        hom = np.hstack([points, np.ones((points.shape[0], 1))])
        new = (S @ hom.T).T[:, :2]
        return new, S
    else:
        tx, ty = about
        T1 = np.array([[1, 0, -tx], [0, 1, -ty], [0, 0, 1]])
        T2 = np.array([[1, 0, tx], [0, 1, ty], [0, 0, 1]])
        M = T2 @ S @ T1
        hom = np.hstack([points, np.ones((points.shape[0], 1))])
        new = (M @ hom.T).T[:, :2]
        return new, M


def reflect(points: np.ndarray, mode: str = "x") -> Tuple[np.ndarray, np.ndarray]:
    if mode == "x":
        M = np.array([[1, 0, 0], [0, -1, 0], [0, 0, 1]])
    elif mode == "y":
        M = np.array([[-1, 0, 0], [0, 1, 0], [0, 0, 1]])
    elif mode == "y=x":
        M = np.array([[0, 1, 0], [1, 0, 0], [0, 0, 1]])
    else:
        # custom line: ax + by + c = 0 reflection requires more work; default to x-axis
        M = np.array([[1, 0, 0], [0, -1, 0], [0, 0, 1]])
    hom = np.hstack([points, np.ones((points.shape[0], 1))])
    new = (M @ hom.T).T[:, :2]
    return new, M


def apply_matrix(points: np.ndarray, M: np.ndarray) -> np.ndarray:
    hom = np.hstack([points, np.ones((points.shape[0], 1))])
    return (M @ hom.T).T[:, :2]


def plot_shapes(original: np.ndarray, transformed: np.ndarray, title1: str = "Original", title2: str = "Transformed"):
    fig, ax = plt.subplots(figsize=(5, 5))
    # Plot original
    poly1 = np.vstack([original, original[0]])
    poly2 = np.vstack([transformed, transformed[0]])
    ax.plot(poly1[:, 0], poly1[:, 1], '-o', label=title1)
    ax.plot(poly2[:, 0], poly2[:, 1], '-o', label=title2)
    # draw axes
    lims = np.max(np.abs(np.vstack([poly1, poly2]))) * 1.5 + 0.1
    if lims == 0:
        lims = 1
    ax.set_xlim(-lims, lims)
    ax.set_ylim(-lims, lims)
    ax.axhline(0, linewidth=0.6)
    ax.axvline(0, linewidth=0.6)
    ax.set_aspect('equal', 'box')
    ax.legend()
    ax.grid(alpha=0.3)
    return fig

# ----------------------------- Streamlit UI -----------------------------

st.title("🔁 Virtual Lab: Transformasi Geometri")
st.markdown("Pelajari rotasi, refleksi, dilatasi, dan translasi secara visual dan interaktif.")

# Layout: sidebar controls + main
with st.sidebar:
    st.header("Pengaturan Bentuk")
    shape = st.selectbox("Pilih bentuk", options=["Segitiga", "Persegi", "Pentagon", "Custom"], index=1)
    if shape == "Segitiga":
        sides = 3
        radius = st.slider("Skala (radius)", 0.5, 3.0, 1.0)
        base_rotation = st.slider("Rotasi awal (derajat)", 0, 360, 0)
    elif shape == "Persegi":
        sides = 4
        radius = st.slider("Skala (radius)", 0.5, 3.0, 1.0)
        base_rotation = st.slider("Rotasi awal (derajat)", 0, 360, 45)
    elif shape == "Pentagon":
        sides = 5
        radius = st.slider("Skala (radius)", 0.5, 3.0, 1.0)
        base_rotation = st.slider("Rotasi awal (derajat)", 0, 360, 0)
    else:
        sides = None
        radius = 1.0
        base_rotation = 0
        st.info("Masukkan koordinat vertex custom sebagai CSV (x,y per baris).")
        custom_text = st.text_area("Koordinat (contoh: 0,0\n1,0\n1,1)", value="0,0\n1,0\n1,1\n0,1")

    st.markdown("---")
    st.header("Pilih Transformasi")
    # Allow stacking transformations in chosen order
    order = st.multiselect("Susunan transformasi (urut dari atas ke bawah)", options=["Translasi", "Rotasi", "Refleksi", "Dilatasi"], default=["Rotasi"])

    # controls for each transform
    st.subheader("Parameter Transformasi")
    # Translasi
    st.markdown("**Translasi**")
    tx = st.number_input("Translasi: geser X (tx)", value=0.0, step=0.5)
    ty = st.number_input("Translasi: geser Y (ty)", value=0.0, step=0.5)

    # Rotasi
    st.markdown("**Rotasi**")
    angle = st.slider("Sudut rotasi (derajat)", -360, 360, 45)
    rot_about_option = st.selectbox("Rotasi tentang", options=["Origin (0,0)", "Centroid bentuk"], index=1)

    # Refleksi
    st.markdown("**Refleksi**")
    reflect_mode = st.selectbox("Refleksi terhadap", options=["x (sumbu-x)", "y (sumbu-y)", "y=x"], index=0)

    # Dilatasi
    st.markdown("**Dilatasi**")
    scale = st.slider("Skala dilatasi (k)", 0.1, 5.0, 1.0)
    dilate_about_option = st.selectbox("Dilatasi tentang", options=["Origin (0,0)", "Centroid bentuk"], index=0)

    st.markdown("---")
    st.subheader("Visualisasi & Output")
    show_matrix = st.checkbox("Tampilkan matriks transformasi gabungan", value=True)
    show_table = st.checkbox("Tampilkan koordinat (sebelum & sesudah)", value=True)
    animate_t = st.slider("Interpolasi animasi (t) — lihat langkah transformasi linier", 0.0, 1.0, 1.0)
    st.markdown("Tekan tombol di bawah untuk menerapkan transformasi")
    apply = st.button("Terapkan transformasi")

# ----------------------------- Prepare points -----------------------------
if sides is not None:
    orig = polygon_points(sides, radius=radius, rotation=base_rotation)
else:
    # parse custom
    try:
        rows = [line.strip() for line in custom_text.strip().splitlines() if line.strip()]
        pts = [list(map(float, r.split(','))) for r in rows]
        orig = np.array(pts)
    except Exception:
        st.error("Format koordinat custom salah — gunakan CSV x,y per baris.")
        st.stop()

# Show original shape info
st.subheader("Bentuk awal")
col1, col2 = st.columns([1, 2])
with col1:
    st.write(f"Jumlah titik: {orig.shape[0]}")
    st.write("Centroid:", tuple(np.round(centroid(orig), 3)))
with col2:
    fig0 = plot_shapes(orig, orig, title1="Bentuk", title2="(preview)")
    st.pyplot(fig0)

# ----------------------------- Apply transformations -----------------------------

# Build combined transformation matrix and transformed points
M_combined = np.eye(3)
current = orig.copy()
steps = []  # store tuples (name, matrix, points)

# Helper: get about point
cent = centroid(orig)
rot_about = None if rot_about_option.startswith('Origin') else cent
dilate_about = None if dilate_about_option.startswith('Origin') else cent

# Apply in selected order
for op in order:
    if op == "Translasi":
        new_pts, M = translate(current, tx, ty)
        steps.append((f"Translasi ({tx}, {ty})", M, new_pts))
        current = new_pts
        M_combined = M @ M_combined
    elif op == "Rotasi":
        new_pts, M = rotate(current, angle, about=(rot_about if rot_about is not None else None))
        # note: rotate function accepts about coordinates from the CURRENT configuration — for clarity,
        # we rotate about centroid of original shape if user chose centroid. To rotate about original centroid
        # for the current points, we convert it to current centroid.
        # For simplicity, we recompute using original centroid translated to current space when needed.
        if rot_about is not None:
            # rotate about centroid of original shape in absolute coordinates
            new_pts, M = rotate(current, angle, about=cent)
        else:
            new_pts, M = rotate(current, angle, about=None)
        steps.append((f"Rotasi ({angle}°) about {'centroid' if rot_about is not None else 'origin'}", M, new_pts))
        current = new_pts
        M_combined = M @ M_combined
    elif op == "Refleksi":
        mode = 'x' if reflect_mode.startswith('x') else ('y' if reflect_mode.startswith('y (sumbu-y)') else 'y=x')
        new_pts, M = reflect(current, mode=('x' if reflect_mode.startswith('x') else ('y' if reflect_mode.startswith('y') and 'sumbu' in reflect_mode else 'y=x')))
        steps.append((f"Refleksi ({reflect_mode})", M, new_pts))
        current = new_pts
        M_combined = M @ M_combined
    elif op == "Dilatasi":
        if dilate_about_option.startswith('Origin'):
            new_pts, M = dilate(current, scale, about=None)
        else:
            new_pts, M = dilate(current, scale, about=cent)
        steps.append((f"Dilatasi (k={scale}) about {'centroid' if dilate_about_option.startswith('Centroid') else 'origin'}", M, new_pts))
        current = new_pts
        M_combined = M @ M_combined

# If no operation selected, current == orig
transformed = current

# Show results
st.subheader("Hasil Transformasi")
colA, colB = st.columns([1, 1])
with colA:
    fig = plot_shapes(orig, transformed, title1="Sebelum", title2="Sesudah")
    st.pyplot(fig)

with colB:
    st.write("**Centroid sebelum -> sesudah**")
    st.write(pd.DataFrame({"x": [np.round(c, 3) for c in [centroid(orig)[0], centroid(transformed)[0]]],
                          "y": [np.round(c, 3) for c in [centroid(orig)[1], centroid(transformed)[1]]]}, index=["Sebelum", "Sesudah"]))

# Show combined matrix if checked
if show_matrix:
    st.subheader("Matriks Transformasi Gabungan (homogen 3x3)")
    st.write(pd.DataFrame(np.round(M_combined, 4)))

# Show step by step
if len(steps) > 0:
    st.subheader("Langkah transformasi")
    for i, (name, M, pts) in enumerate(steps, 1):
        st.markdown(f"**{i}. {name}**")
        st.write("Matriks:")
        st.write(pd.DataFrame(np.round(M, 4)))
        fig_step = plot_shapes(orig if i==1 else steps[i-2][2], pts, title1=("Sebelum" if i==1 else f"Setelah langkah {i-1}"), title2=(f"Setelah {i}"))
        st.pyplot(fig_step)

# Show coordinates table
if show_table:
    st.subheader("Koordinat titik")
    df_coords = pd.DataFrame(np.hstack([orig, transformed]), columns=["x_before", "y_before", "x_after", "y_after"])
    st.dataframe(df_coords.style.format(precision=3))

# Animation / interpolation: linear interpolation between orig and transformed
if animate_t < 1.0:
    interp = orig + animate_t * (transformed - orig)
    st.subheader(f"Interpolasi t={animate_t:.2f}")
    fig_interp = plot_shapes(orig, interp, title1="Sebelum", title2=f"Interpolasi t={animate_t:.2f}")
    st.pyplot(fig_interp)

# Download button: save plot of before/after
buf = io.BytesIO()
fig_export = plot_shapes(orig, transformed, title1="Sebelum", title2="Sesudah")
fig_export.savefig(buf, format='png', bbox_inches='tight')
buf.seek(0)

st.download_button("Unduh gambar hasil (PNG)", data=buf, file_name="transformasi_hasil.png", mime="image/png")

st.markdown("---")
st.info("Catatan: Anda dapat mengubah susunan transformasi di sidebar untuk melihat bagaimana urutan mempengaruhi hasil. Untuk refleksi terhadap garis custom atau transformasi lebih kompleks, Anda dapat memodifikasi fungsi `reflect` di kode.")

# End of app



# If run as script, streamlit will launch the app.
if __name__ == '__main__':
    pass
