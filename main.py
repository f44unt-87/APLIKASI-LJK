import streamlit as st
import cv2
import numpy as np

# --- SETTING PRESISI (Ubah angka ini sedikit demi sedikit) ---
# START_Y = posisi y nomor 1, ROW_GAP = jarak antar baris, COL_GAP = jarak antar kolom
START_Y = 350  # Coba ubah angka ini agar baris 1 pas
ROW_GAP = 30   # Jarak vertikal antar baris
COL_GAP = 30   # Jarak horizontal antar kolom A-B-C-D-E
START_X = 220  # Coba ubah angka ini agar kolom A pas
# ------------------------------------------------------------

def proses_ljk(image_file):
    file_bytes = np.asarray(bytearray(image_file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, 1)
    vis = img.copy()
    hasil = {}
    
    for i in range(1, 51):
        # Logika pembagian kolom (10 nomor per kolom)
        col = (i - 1) // 10 
        row = (i - 1) % 10
        
        base_x = START_X + (col * (COL_GAP * 7)) # 7 adalah jarak antar kolom utama
        base_y = START_Y + (row * ROW_GAP)
        
        hasil[i] = "-"
        max_d = 0
        
        for j, opt in enumerate(['A','B','C','D','E']):
            x = int(base_x + (j * COL_GAP))
            y = int(base_y)
            
            # Gambar lingkaran untuk panduan kalibrasi
            cv2.circle(vis, (x, y), 10, (0, 0, 255), 2)
            
            roi = img[y-15:y+15, x-15:x+15]
            if roi.size == 0: continue
            
            gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
            _, thresh = cv2.threshold(gray_roi, 120, 255, cv2.THRESH_BINARY_INV)
            d = cv2.countNonZero(thresh) / thresh.size
            
            if d > 0.15 and d > max_d:
                max_d = d
                hasil[i] = opt
    return hasil, vis

st.title("Sistem Koreksi LJK Presisi")
up = st.file_uploader("Upload LJK", type=['jpg', 'png'])
if up and st.button("Proses"):
    res, vis = proses_ljk(up)
    st.json(res)
    st.image(cv2.cvtColor(vis, cv2.COLOR_BGR2RGB))
