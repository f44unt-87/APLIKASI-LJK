import streamlit as st
import cv2
import numpy as np
import json

# 1. FUNGSI UNTUK MENDETEKSI GRID OTOMATIS
def proses_ljk(image_file):
    # Load gambar
    file_bytes = np.asarray(bytearray(image_file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, 1)
    
    # Deteksi sudut untuk pelurusan
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Ambil kontur terbesar (kertas)
    kontur = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(kontur)
    
    # Crop kertas saja
    img_crop = img[y:y+h, x:x+w]
    vis = img_crop.copy()
    
    # 2. LOGIKA GRID (Ini yang membuat pas)
    # Kita bagi area LJK menjadi grid otomatis berdasarkan lebar/tinggi
    # Tidak perlu koordinat fix yang meleset lagi
    hasil = {}
    kolom_width = w // 5
    baris_height = h // 55 # Estimasi 50 nomor + header
    
    # Contoh visualisasi grid untuk kalibrasi
    for i in range(1, 51):
        hasil[i] = "-"
        # Menentukan posisi Y berdasarkan nomor (1-50)
        y_pos = int(h * 0.15 + (i * (h * 0.75 / 50)))
        
        # Cek 5 opsi (A, B, C, D, E) per baris
        for j, opt in enumerate(['A','B','C','D','E']):
            x_pos = int(w * 0.15 + (j * (w * 0.6 / 5)))
            
            # Gambar lingkaran panduan agar Anda bisa lihat posisinya
            cv2.circle(vis, (x_pos, y_pos), 12, (0, 0, 255), 2)
            
            # Deteksi hitam
            roi = img_crop[y_pos-15:y_pos+15, x_pos-15:x_pos+15]
            if roi.size == 0: continue
            
            gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
            _, thresh_roi = cv2.threshold(gray_roi, 120, 255, cv2.THRESH_BINARY_INV)
            d = cv2.countNonZero(thresh_roi) / thresh_roi.size
            
            if d > 0.15: # sensitivitas
                hasil[i] = opt
                
    return hasil, vis

# 3. UI
st.title("Sistem Koreksi LJK Presisi")
up = st.file_uploader("Upload LJK", type=['jpg', 'png'])
if up and st.button("Proses"):
    res, vis = proses_ljk(up)
    st.json(res)
    st.image(cv2.cvtColor(vis, cv2.COLOR_BGR2RGB))
