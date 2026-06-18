import streamlit as st
import cv2
import numpy as np
import json
import os

# 1. KONFIGURASI
OFFSET_X = -60
OFFSET_Y = -40

# 2. PROSES UTAMA
def proses_gambar(image):
    file_bytes = np.asarray(bytearray(image.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, 1)
    
    # Perbaikan: Tambahkan fungsi luruskan_gambar di sini (seperti kode sebelumnya)
    vis = img.copy() 
    hasil = {}
    
    with open('template_coords.json', 'r') as f:
        KOORDINAT = json.load(f)
    
    for no, pilihan in KOORDINAT.items():
        hasil[no] = "-"
        max_d = 0
        
        # MEMASTIKAN 5 LINGKARAN TERBACA
        # Kita ambil kunci (A, B, C, D, E) langsung dari data nomor tersebut
        opsi_list = sorted(pilihan.keys()) 
        
        for opt in opsi_list:
            x_raw, y_raw = pilihan[opt]
            # Menghitung posisi
            x = int(x_raw + OFFSET_X)
            y = int(y_raw + OFFSET_Y + (int(no) * 0.1))
            
            # VISUALISASI: Lingkaran merah diperkecil radiusnya (menjadi 10) 
            # agar tidak tumpang tindih
            cv2.circle(vis, (x, y), 10, (0, 0, 255), 2)
            cv2.putText(vis, opt, (x-5, y-15), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0,0,255), 1)
            
            roi = img[y-20:y+20, x-20:x+20]
            if roi.size == 0: continue
            
            gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
            _, thresh = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY_INV)
            d = cv2.countNonZero(thresh) / thresh.size
            
            if d > 0.20 and d > max_d:
                max_d = d
                hasil[no] = opt
                
    return hasil, vis

# 3. UI
st.title("Koreksi LJK")
up = st.file_uploader("Upload", type=['jpg', 'png'])
if up and st.button("Proses"):
    res, vis = proses_gambar(up)
    st.json(res)
    st.image(cv2.cvtColor(vis, cv2.COLOR_BGR2RGB))
