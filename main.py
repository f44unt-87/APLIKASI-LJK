import streamlit as st
import cv2
import numpy as np

# KONFIGURASI LAYOUT:
# Ubah nilai-nilai di bawah ini jika lingkaran merah masih meleset 1-2 pixel
START_X = 230   # Titik X nomor 1, kolom A
START_Y = 360   # Titik Y nomor 1, kolom A
GAP_X = 35      # Jarak antar kolom (A-B, B-C, dst)
GAP_Y = 32      # Jarak antar baris (Nomor 1-2, 2-3, dst)

st.title("Koreksi LJK Final")
up = st.file_uploader("Upload Foto LJK", type=['jpg', 'png'])

if up and st.button("Proses Koreksi"):
    img = cv2.imdecode(np.asarray(bytearray(up.read()), dtype=np.uint8), 1)
    # Resize ke ukuran standar agar koordinat tidak berubah-ubah
    img = cv2.resize(img, (800, 1000)) 
    vis = img.copy()
    hasil = {}

    for i in range(1, 51):
        # Logika pembagian kolom (10 nomor per kolom)
        col = (i - 1) // 10
        row = (i - 1) % 10
        
        # Hitung posisi X dan Y
        base_x = START_X + (col * GAP_X * 6)
        base_y = START_Y + (row * GAP_Y)
        
        jawaban = "-"
        max_d = 0
        
        for j, opt in enumerate(['A','B','C','D','E']):
            x = int(base_x + (j * GAP_X))
            y = int(base_y)
            
            # Gambar lingkaran merah sebagai panduan
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

    st.json(hasil)
    st.image(cv2.cvtColor(vis, cv2.COLOR_BGR2RGB))
