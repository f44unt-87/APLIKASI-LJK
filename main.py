import streamlit as st
import cv2
import numpy as np

# KONFIGURASI GRID (Berdasarkan titik acuan di atas)
START_X = 246
START_Y = 438
COL_GAP = 32  # Jarak antar A-B-C-D-E
ROW_GAP = 43  # Jarak antar nomor (1 ke 2)
COL_SHIFT = 237 # Jarak geser ke kolom berikutnya (kolom 1 ke 2)

def proses_ljk(image_file):
    file_bytes = np.asarray(bytearray(image_file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, 1)
    vis = img.copy()
    hasil = {}
    
    for i in range(1, 51):
        # Logika menghitung posisi setiap nomor (1-50)
        # LJK Anda: 1-10 (kolom1), 11-20 (kolom2), dst.
        kolom = (i - 1) // 10
        baris = (i - 1) % 10
        
        base_x = START_X + (kolom * COL_SHIFT)
        base_y = START_Y + (baris * ROW_GAP)
        
        jawaban = "-"
        max_d = 0
        
        for j, opt in enumerate(['A','B','C','D','E']):
            x = int(base_x + (j * COL_GAP))
            y = int(base_y)
            
            # Gambar lingkaran panduan
            cv2.circle(vis, (x, y), 12, (0, 0, 255), 2)
            
            # Deteksi hitam
            roi = img[y-15:y+15, x-15:x+15]
            if roi.size == 0: continue
            
            gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
            _, thresh = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY_INV)
            d = cv2.countNonZero(thresh) / thresh.size
            
            if d > 0.15 and d > max_d:
                max_d = d
                jawaban = opt
        hasil[i] = jawaban
    return hasil, vis

st.title("Koreksi LJK Presisi")
up = st.file_uploader("Upload LJK", type=['jpg', 'png'])
if up and st.button("Proses"):
    res, vis = proses_ljk(up)
    st.json(res)
    st.image(cv2.cvtColor(vis, cv2.COLOR_BGR2RGB))
