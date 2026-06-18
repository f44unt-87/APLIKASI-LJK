import streamlit as st
import cv2
import numpy as np
import json
import os

# 1. KONFIGURASI PATH (Paling Aman)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(BASE_DIR, 'template_coords.json')

# 2. DEBUGGING: Memastikan file terlihat oleh sistem
st.title("Koreksi LJK Maslakul Huda")
files_in_dir = os.listdir(BASE_DIR)
# Uncomment baris di bawah jika masih error 'File Not Found'
# st.write(f"DEBUG: File yang terbaca di folder: {files_in_dir}")

# 3. LOAD DATA KOORDINAT
if 'template_coords.json' not in files_in_dir:
    st.error(f"File template_coords.json TIDAK DITEMUKAN di {BASE_DIR}. Pastikan file sudah di-upload ke GitHub root.")
    st.stop()

with open(FILE_PATH, 'r') as f:
    KOORDINAT = json.load(f)

# 4. FUNGSI LOGIKA DETEKSI (Inti Koreksi)
def proses_gambar(image):
    # Konversi foto stream ke format OpenCV
    file_bytes = np.asarray(bytearray(image.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, 1)
    
    hasil_jawaban = {}
    
    # Loop melalui koordinat yang ada di JSON
    for no, pilihan in KOORDINAT.items():
        jawaban_terpilih = "-"
        max_density = 0
        
        for opsi, (x, y) in pilihan.items():
            # Mengambil area (ROI) 30x30 piksel
            roi = img[y-15:y+15, x-15:x+15]
            
            gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
            _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
            
            # Hitung persentase piksel hitam
            kepadatan = cv2.countNonZero(thresh) / thresh.size
            
            # Ambang batas 30% untuk deteksi coretan
            if kepadatan > 0.3 and kepadatan > max_density:
                max_density = kepadatan
                jawaban_terpilih = opsi
        
        hasil_jawaban[no] = jawaban_terpilih
    
    return hasil_jawaban

# 5. TAMPILAN FRONTEND
uploaded_file = st.file_uploader("Upload Foto LJK", type=['jpg', 'png', 'jpeg'])

if uploaded_file:
    st.image(uploaded_file, caption='Foto LJK yang diunggah')
    if st.button("Mulai Koreksi"):
        try:
            hasil = proses_gambar(uploaded_file)
            st.success("Hasil Koreksi:")
            st.write(hasil) # Menampilkan hasil dalam bentuk tabel/dict
        except Exception as e:
            st.error(f"Terjadi kesalahan saat memproses gambar: {e}")
