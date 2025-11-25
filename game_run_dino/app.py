import streamlit as st
import time
import random
import numpy as np
import matplotlib.pyplot as plt

# --- Game Configuration ---
GROUND_LEVEL = 0.1  # Posisi Y tanah
RUNNER_SIZE = 0.5   # Ukuran pelari (tinggi)
OBSTACLE_HEIGHT_MIN = 0.3
OBSTACLE_HEIGHT_MAX = 0.8
OBSTACLE_WIDTH = 0.3
JUMP_STRENGTH = 0.8 # Kekuatan lompatan awal
GRAVITY = 0.08      # Kekuatan gravitasi
GAME_SPEED = 0.08   # Kecepatan game (detik per frame)
OBSTACLE_SPAWN_RATE = 0.02 # Probabilitas rintangan muncul setiap frame

# --- Warna Keren ---
COLOR_BACKGROUND = '#87CEEB' # Sky Blue
COLOR_GROUND = '#228B22'     # Forest Green
COLOR_RUNNER = '#FF4500'     # Orange Red
COLOR_OBSTACLE = '#6A5ACD'   # Slate Blue
COLOR_TEXT = '#FFFFFF'       # White

# --- State Game Awal ---
if 'game_started' not in st.session_state:
    st.session_state.game_started = False
    st.session_state.runner_y = GROUND_LEVEL
    st.session_state.runner_vy = 0 # Kecepatan vertikal pelari
    st.session_state.obstacles = [] # Daftar rintangan: [(x, y, width, height), ...]
    st.session_state.score = 0
    st.session_state.frame_count = 0
    st.session_state.game_over = False

def reset_game():
    st.session_state.game_started = True
    st.session_state.runner_y = GROUND_LEVEL
    st.session_state.runner_vy = 0
    st.session_state.obstacles = []
    st.session_state.score = 0
    st.session_state.frame_count = 0
    st.session_state.game_over = False

def update_game_state():
    if st.session_state.game_over:
        return

    # Update Runner Position (Jump & Gravity)
    st.session_state.runner_y += st.session_state.runner_vy
    st.session_state.runner_vy -= GRAVITY # Gravitasi menarik ke bawah

    if st.session_state.runner_y <= GROUND_LEVEL:
        st.session_state.runner_y = GROUND_LEVEL
        st.session_state.runner_vy = 0

    # Update Obstacles
    new_obstacles = []
    for obs_x, obs_y, obs_w, obs_h in st.session_state.obstacles:
        obs_x -= 0.1 # Rintangan bergerak ke kiri
        if obs_x > -OBSTACLE_WIDTH: # Hapus rintangan yang sudah keluar layar
            new_obstacles.append((obs_x, obs_y, obs_w, obs_h))
    st.session_state.obstacles = new_obstacles

    # Spawn New Obstacle
    if random.random() < OBSTACLE_SPAWN_RATE and len(st.session_state.obstacles) < 2:
        if not st.session_state.obstacles or st.session_state.obstacles[-1][0] < 0.7: # Pastikan ada jarak antar rintangan
            obs_height = random.uniform(OBSTACLE_HEIGHT_MIN, OBSTACLE_HEIGHT_MAX)
            st.session_state.obstacles.append((1.0, GROUND_LEVEL, OBSTACLE_WIDTH, obs_height)) # x=1.0 adalah batas kanan layar

    # Collision Detection
    runner_hitbox = {
        'x_min': 0.1, 'x_max': 0.1 + RUNNER_SIZE/2,
        'y_min': st.session_state.runner_y, 'y_max': st.session_state.runner_y + RUNNER_SIZE
    }
    
    for obs_x, obs_y, obs_w, obs_h in st.session_state.obstacles:
        obstacle_hitbox = {
            'x_min': obs_x, 'x_max': obs_x + obs_w,
            'y_min': obs_y, 'y_max': obs_y + obs_h
        }

        if (runner_hitbox['x_max'] > obstacle_hitbox['x_min'] and
            runner_hitbox['x_min'] < obstacle_hitbox['x_max'] and
            runner_hitbox['y_max'] > obstacle_hitbox['y_min'] and
            runner_hitbox['y_min'] < obstacle_hitbox['y_max']):
            
            st.session_state.game_over = True
            break
            
    # Update Score
    st.session_state.score += 1
    st.session_state.frame_count += 1

def jump():
    if st.session_state.runner_y == GROUND_LEVEL and not st.session_state.game_over:
        st.session_state.runner_vy = JUMP_STRENGTH

# --- Streamlit UI ---
st.set_page_config(
    page_title="Pixel Runner",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.title("🏃‍♂️ Pixel Runner: Game Lompat Menarik!")

# Placeholder untuk game
game_placeholder = st.empty()

# Tombol untuk memulai/melompat
col_buttons = st.columns([1, 1, 1])
with col_buttons[1]: # Tengah
    if not st.session_state.game_started:
        if st.button("Mulai Game Baru", key="start_game_btn", help="Klik untuk memulai petualangan!"):
            reset_game()
            st.rerun() # Penting untuk me-restart loop game
    elif st.session_state.game_over:
        st.error(f"GAME OVER! Skor Anda: {st.session_state.score}")
        if st.button("Main Lagi?", key="restart_game_btn", help="Coba lagi untuk skor lebih tinggi!"):
            reset_game()
            st.rerun()
    else:
        if st.button("Lompat!", key="jump_btn", help="Tekan untuk membuat pelari melompat!"):
            jump()
            # Tidak perlu st.rerun() di sini, karena game loop akan memanggilnya
        # Tombol lompat tidak perlu rerun karena game loop akan terus berjalan
        # dan update_game_state akan dipanggil setiap iterasi

if st.session_state.game_started and not st.session_state.game_over:
    st.sidebar.markdown(f"**SKOR:** `{st.session_state.score}`")
    st.sidebar.markdown("Tekan tombol 'Lompat!' atau gunakan spasi (jika bisa diimplementasikan pada browser Anda).") # Spasi mungkin tidak langsung berfungsi di Streamlit
    
    # Loop Game Utama
    with game_placeholder.container():
        # Update state
        update_game_state()

        # Render Game (Matplotlib)
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.set_facecolor(COLOR_BACKGROUND)
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off') # Sembunyikan sumbu

        # Gambar Tanah
        ax.hlines(GROUND_LEVEL, 0, 1, color=COLOR_GROUND, linewidth=20)
        
        # Gambar Pelari
        runner_x = 0.1 # Posisi X pelari tetap
        runner_y_draw = st.session_state.runner_y + GROUND_LEVEL # Sesuaikan untuk dasar tanah
        ax.add_patch(plt.Rectangle((runner_x, runner_y_draw), RUNNER_SIZE/2, RUNNER_SIZE, color=COLOR_RUNNER, zorder=3))

        # Gambar Rintangan
        for obs_x, obs_y, obs_w, obs_h in st.session_state.obstacles:
            ax.add_patch(plt.Rectangle((obs_x, obs_y + GROUND_LEVEL), obs_w, obs_h, color=COLOR_OBSTACLE, zorder=2))
        
        # Tampilkan Skor di dalam game
        ax.text(0.95, 0.9, f"SKOR: {st.session_state.score}", 
                horizontalalignment='right', verticalalignment='top', 
                color=COLOR_TEXT, fontsize=16, 
                bbox=dict(facecolor='black', alpha=0.5, edgecolor='none', boxstyle='round,pad=0.5'))

        st.pyplot(fig)
        plt.close(fig) # Penting untuk membebaskan memori

    # Force rerun untuk loop game
    time.sleep(GAME_SPEED)
    st.rerun()

elif not st.session_state.game_started:
    with game_placeholder.container():
        st.info("Klik 'Mulai Game Baru' untuk bermain!")
        st.image("https://images.unsplash.com/photo-1605379399642-870262d3d051?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1770&q=80", 
                 caption="Siap berlari? Gambar oleh Vova Valuysky di Unsplash", use_column_width=True)

# Footer
st.markdown("---")
st.markdown("Dibuat dengan ❤️ oleh AI & Streamlit")
