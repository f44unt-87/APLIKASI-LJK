import streamlit as st
import cv2
import numpy as np

# --- KONFIGURASI PRESISI (UBAH ANGKA INI JIKA POSISI MELSET) ---
# START_X, START_Y: Titik tengah lingkaran 1-A
# COL_GAP: Jarak horizontal antar lingkaran (A ke B, B ke C, dst)
# ROW_GAP: Jarak vertikal antar nomor (1 ke 2)
# COL_SHIFT: Jarak lompatan horizontal ke kelompok nomor berikutnya (10 ke 11)
START_X, START_Y = 145, 340 
COL_GAP = 30
ROW_GAP = 35
COL_SHIFT = 230
# --------------------------------------------------------------

def proses_ljk(image_file):
    file_bytes = np.asarray(bytearray(image_file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, 1)
    vis = img.copy()
    hasil = {}
    
    for i in range(1, 51):
        # Membagi 50 nomor menjadi 5 kelompok kolom (1-10, 11-20, dst)
        kolom = (i - 1) // 10
        baris = (i - 1) % 10
        
        base_x = START_X + (kolom * COL_SHIFT)
        base_y = START_Y + (baris * ROW_GAP)
        
        jawaban = "-"
        max_d = 0
        
        # Selalu memproses 5 pilihan (A, B, C, D, E)
        for j, opt in enumerate(['A', 'B', 'C', 'D', 'E']):
            x = int(base_x + (j * COL_GAP))
            y = int(base_y)
            
            # Gambar lingkaran panduan merah untuk kalibrasi
            cv2.circle(vis, (x, y), 12, (0, 0, 255), 2)
            
            # Deteksi kepadatan piksel hitam
            roi = img[y-12:y+12, x-12:x+12]
            if roi.size == 0: continue
            
            gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
            _, thresh = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY_INV)
            d = cv2.countNonZero(thresh) / thresh.size
            
            # Ambang batas deteksi (0.15 berarti 15% area harus hitam)
            if d > 0.15 and d > max_d:
                max_d = d
                jawaban = opt
        hasil[i] = jawaban
    return hasil, vis

st.title("Koreksi LJK - Maslakul Huda")
up = st.file_uploader("Upload Foto LJK", type=['jpg', 'png', 'jpeg'])

if up and st.button("Proses Koreksi"):
    res, vis = proses_ljk(up)
    st.json(res)
    st.image(cv2.cvtColor(vis, cv2.COLOR_BGR2RGB), use_column_width=True)
