import streamlit as st
import numpy as np
import random

# --- Konfigurasi Warna & Gaya ---
COLOR_BACKGROUND = '#F0F2F6'
COLOR_HEADER = '#4B0082'  # Indigo
COLOR_BUTTON = '#FF6347'  # Tomato
COLOR_GIVEN = '#D3D3D3'   # Light Gray
COLOR_INPUT = '#FFFFFF'   # White
COLOR_VALID = '#E0FFFF'   # Azure
COLOR_INVALID = '#FFB6C1' # Light Pink

# --- Logika Sudoku ---

def generate_sudoku(k):
    """Membuat papan Sudoku yang terpecahkan dan menghilangkan k angka."""
    board = np.zeros((9, 9), dtype=int)
    
    # Isi diagonal 3x3 box untuk memastikan solusi awal yang unik
    def fill_box(r, c):
        nums = random.sample(range(1, 10), 9)
        for i in range(3):
            for j in range(3):
                board[r + i, c + j] = nums.pop()

    fill_box(0, 0)
    fill_box(3, 3)
    fill_box(6, 6)

    # Memecahkan sisa papan
    def solve_sudoku_util():
        for r in range(9):
            for c in range(9):
                if board[r, c] == 0:
                    for num in random.sample(range(1, 10), 9):
                        if is_valid_move(board, r, c, num):
                            board[r, c] = num
                            if solve_sudoku_util():
                                return True
                            board[r, c] = 0  # Backtrack
                    return False
        return True
    
    solve_sudoku_util()
    
    # Simpan solusi untuk pemeriksaan nanti
    solution = board.copy()
    
    # Menghilangkan k angka untuk membuat puzzle
    cells = [(r, c) for r in range(9) for c in range(9)]
    random.shuffle(cells)
    
    for r, c in cells:
        if k <= 0:
            break
        board[r, c] = 0
        k -= 1
        
    return board, solution

def is_valid_move(board, row, col, num):
    """Cek apakah angka valid untuk ditempatkan di posisi (row, col)"""
    
    # Cek baris
    if num in board[row, :]:
        return False
        
    # Cek kolom
    if num in board[:, col]:
        return False
        
    # Cek 3x3 box
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    if num in board[start_row:start_row + 3, start_col:start_col + 3]:
        return False
        
    return True

# --- Fungsi Game Streamlit ---

def initialize_game():
    """Menginisialisasi state game baru."""
    # Jumlah sel yang dihilangkan (kesulitan)
    difficulty = st.session_state.get('difficulty', 40) 
    
    # 1. Buat papan dan solusinya
    puzzle, solution = generate_sudoku(difficulty)
    
    # 2. Simpan ke session state
    st.session_state.puzzle = puzzle.copy()
    st.session_state.user_board = puzzle.copy()
    st.session_state.solution = solution
    
    # 3. Tentukan sel yang diberikan (tidak bisa diubah)
    st.session_state.given_mask = (puzzle != 0)
    st.session_state.game_over = False
    st.session_state.message = "Selamat Bermain! Isi kotak yang kosong."

def check_game():
    """Memeriksa apakah papan pengguna benar dan lengkap."""
    if np.array_equal(st.session_state.user_board, st.session_state.solution):
        st.session_state.game_over = True
        st.session_state.message = "🎉 SELAMAT! Anda memecahkan Sudoku ini dengan benar!"
    elif np.count_nonzero(st.session_state.user_board == 0) == 0:
         st.session_state.message = "Papan lengkap, tetapi masih ada kesalahan!"
    else:
        st.session_state.message = "Papan diperbarui. Terus semangat!"

def get_cell_color(r, c):
    """Mendapatkan warna latar belakang untuk sel berdasarkan statusnya."""
    if st.session_state.given_mask[r, c]:
        # Angka yang sudah ada (diberikan)
        return COLOR_GIVEN
    
    current_val = st.session_state.user_board[r, c]
    if current_val == 0:
        # Sel kosong
        return COLOR_INPUT
    
    # Cek validitas angka yang dimasukkan pengguna
    if current_val == st.session_state.solution[r, c]:
        return COLOR_VALID
    else:
        return COLOR_INVALID

def handle_input(r, c):
    """Mengelola input dari pengguna di sel (r, c)."""
    # Ambil nilai dari key input
    try:
        val = int(st.session_state[f'input_{r}_{c}'])
        if 1 <= val <= 9:
            st.session_state.user_board[r, c] = val
        else:
             st.session_state.user_board[r, c] = 0 # Kosongkan jika bukan 1-9
    except:
        st.session_state.user_board[r, c] = 0 # Kosongkan jika bukan angka
    
    # Setelah input, periksa status game
    check_game()

# --- Setup Streamlit UI ---

st.set_page_config(
    page_title="Sudoku Interaktif",
    layout="centered",
    initial_sidebar_state="expanded"
)

st.markdown(f"""
    <style>
    .stApp {{background-color: {COLOR_BACKGROUND};}}
    h1 {{color: {COLOR_HEADER}; text-align: center;}}
    .stButton>button {{
        background-color: {COLOR_BUTTON}; 
        color: white;
        border-radius: 8px;
        font-weight: bold;
        padding: 10px 20px;
    }}
    .stTable, .stDataFrame {{
        border: 4px solid #333333; /* Border luar papan */
    }}
    </style>
""", unsafe_allow_html=True)

st.title("🔢 Sudoku Interaktif Berwarna")

# Inisialisasi Game jika belum ada
if 'puzzle' not in st.session_state:
    initialize_game()

# --- Sidebar Kontrol ---
with st.sidebar:
    st.header("Kontrol Permainan")
    
    # Pilihan Kesulitan
    st.markdown("---")
    st.subheader("Tingkat Kesulitan")
    difficulty_mapping = {
        "Mudah": 30,  # Lebih banyak angka yang diberikan
        "Sedang": 40,
        "Sulit": 50,  # Lebih sedikit angka yang diberikan
    }
    
    difficulty_label = st.selectbox("Pilih kesulitan:", list(difficulty_mapping.keys()), index=1)
    st.session_state.difficulty = difficulty_mapping[difficulty_label]
    
    # Tombol Aksi
    st.markdown("---")
    if st.button("Mulai Game Baru", on_click=initialize_game):
        st.experimental_rerun() # Rerun untuk memuat papan baru
        
    st.markdown("---")
    if st.button("Tampilkan Solusi 💡"):
        st.session_state.user_board = st.session_state.solution.copy()
        st.session_state.game_over = True
        st.session_state.message = "Ini Solusinya. Game Selesai."


# --- Area Game Utama ---
st.markdown(f"**Status:** *{st.session_state.message}*", unsafe_allow_html=True)

# Grid Sudoku (9 kolom)
cols = st.columns(9)

# Iterasi untuk mengisi sel
for r in range(9):
    for c in range(9):
        # Tentukan style sel berdasarkan posisi dan box 3x3
        style = f"background-color: {get_cell_color(r, c)}; text-align: center; padding: 5px;"
        
        # Tambahkan border tebal untuk memisahkan box 3x3
        if c % 3 == 0 and c != 0:
            style += " border-left: 3px solid #333333;"
        if r % 3 == 0 and r != 0:
            style += " border-top: 3px solid #333333;"
        
        with cols[c]:
            if st.session_state.given_mask[r, c]:
                # Sel yang Diberikan (angka tebal, tidak bisa diubah)
                st.markdown(f"""
                    <div style="{style} font-weight: bold; color: #333333; height: 40px; line-height: 40px;">
                        {st.session_state.puzzle[r, c]}
                    </div>
                """, unsafe_allow_html=True)
            else:
                # Sel Input Pengguna
                st.text_input(
                    label=' ',
                    value=str(st.session_state.user_board[r, c]) if st.session_state.user_board[r, c] != 0 else '',
                    max_chars=1,
                    key=f'input_{r}_{c}',
                    on_change=handle_input,
                    args=(r, c),
                    disabled=st.session_state.game_over,
                    help="Masukkan angka 1-9"
                )
                
# Info dan Tips
st.markdown("---")
st.markdown("#### Tips Mewarnai:")
st.markdown(f"""
* Kotak **Abu-abu Muda ({COLOR_GIVEN})**: Angka awal yang tidak bisa diubah.
* Kotak **Putih ({COLOR_INPUT})**: Sel kosong yang harus diisi.
* Kotak **Hijau Pucat ({COLOR_VALID})**: Angka yang Anda masukkan **sudah benar**.
* Kotak **Merah Muda ({COLOR_INVALID})**: Angka yang Anda masukkan **salah**.
""")
