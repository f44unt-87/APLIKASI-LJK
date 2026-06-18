import streamlit as st
import cv2
import numpy as np

def proses_ljk(image_file):
    file_bytes = np.asarray(bytearray(image_file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, 1)
    
    # 1. Resize agar ukuran selalu tetap (800x1000), ini kunci agar tidak kecil
    img = cv2.resize(img, (800, 1000))
    vis = img.copy()
    
    # 2. KONFIGURASI PRESISI (Untuk gambar 800x1000)
    START_X, START_Y = 100, 150 
    ROW_GAP = 32
    COL_GAP = 35
    
    hasil = {}
    
    for i in range(1, 51):
        col = (i - 1) // 10
        row = (i - 1) % 10
        
        # Kelompokkan menjadi 5 kolom (10 nomor per kolom)
        base_x = START_X + (col * (COL_GAP * 6))
        base_y = START_Y + (row * ROW_GAP)
        
        hasil[i] = "-"
        max_d = 0
        
        for j, opt in enumerate(['A','B','C','D','E']):
            x = int(base_x + (j * COL_GAP))
            y = int(base_y)
            
            # Gambar lingkaran panduan
            cv2.circle(vis, (x, y), 12, (0, 0, 255), 2)
            
            roi = img[y-15:y+15, x-15:x+15]
            if roi.size == 0: continue
            
            gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
            _, thresh = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY_INV)
            d = cv2.countNonZero(thresh) / roi.size
            
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
