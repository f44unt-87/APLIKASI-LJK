import streamlit as st
import cv2
import numpy as np
import json
import os

# 1. KONFIGURASI PATH
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(BASE_DIR, 'template_coords.json')

# 2. LOAD DATA KOORDINAT DENGAN ERROR HANDLING
if not os.path.exists(FILE_PATH):
    st.error(f"File {FILE_PATH} tidak ditemukan! Pastikan file berada di root folder GitHub.")
    st.stop()

with open(FILE_PATH, 'r') as f:
    KOORDINAT = json.load(f)

# 3. FUNGSI LOGIKA DETEKSI
def proses_gambar(image):
    file_bytes = np.asarray(bytearray(image.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, 1)
    
    hasil_jawaban = {}
    
    # Loop melalui koordinat yang ada di JSON
    for no, pilihan in KOORDINAT.items():
        jawaban_terpilih = "-"
        max_density = 0
        
        for opsi, (x, y) in pilihan.items():
            # Mengambil area lingkaran (ROI)
            # Pastikan koordinat x,y di JSON sesuai dengan skala foto yang diupload
            roi = img[y-15:y+15, x-15:x+15]
            
            gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
            _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
            
            kepadatan = cv2.countNonZero(thresh) / thresh.size
            
            if kepadatan > 0.3 and kepadatan > max_density:
                max_density = kepadatan
                jawaban_terpilih = opsi
        
        hasil_jawaban[no] = jawaban_terpilih
    
    return hasil_jawaban

# 4. TAMPILAN FRONTEND
st.title("Koreksi LJK Maslakul Huda")
uploaded_file = st.file_uploader("Upload Foto LJK", type=['jpg', 'png', 'jpeg'])

if uploaded_file:
    st.image(uploaded_file, caption='Foto LJK yang diunggah')
    if st.button("Mulai Koreksi"):
        try:
            hasil = proses_gambar(uploaded_file)
            st.success("Hasil Koreksi:")
            st.json(hasil)
        except Exception as e:
            st.error(f"Terjadi kesalahan saat memproses gambar: {e}")
