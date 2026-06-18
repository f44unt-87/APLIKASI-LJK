import streamlit as st
import cv2
import numpy as np
import json
import os


# Mendapatkan direktori tempat main.py berada
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(BASE_DIR, 'template_coords.json')

# Memuat koordinat menggunakan path lengkap
with open(FILE_PATH, 'r') as f:
    KOORDINAT = json.load(f)

def proses_gambar(image):
    # Konversi file upload ke format OpenCV
    file_bytes = np.asarray(bytearray(image.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, 1)
    
    # [LOGIKA] Di sini nanti Anda tambahkan Warp Perspective
    # Setelah gambar diluruskan, kita cek kepadatan pixel di setiap koordinat
    hasil_koreksi = {}
    for no, pilihan in KOORDINAT.items():
        skor_tertinggi = 0
        jawaban_terpilih = "-"
        for ops, (x, y) in pilihan.items():
            # Ambil potongan area lingkaran (ROI)
            roi = img[y-15:y+15, x-15:x+15]
            gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
            _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
            kepadatan = cv2.countNonZero(thresh) / thresh.size
            
            if kepadatan > 0.3 and kepadatan > skor_tertinggi:
                skor_tertinggi = kepadatan
                jawaban_terpilih = ops
        hasil_koreksi[no] = jawaban_terpilih
    return hasil_koreksi

# Tampilan Streamlit
st.title("Koreksi LJK Maslakul Huda")
uploaded_file = st.file_uploader("Upload Foto LJK", type=['jpg', 'png'])

if uploaded_file:
    st.image(uploaded_file)
    if st.button("Mulai Koreksi"):
        hasil = proses_gambar(uploaded_file)
        st.write("Hasil Jawaban:", hasil)
