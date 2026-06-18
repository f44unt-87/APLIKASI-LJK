import streamlit as st
import cv2
import numpy as np
import json
import os

st.title("Koreksi LJK Maslakul Huda")

# --- DEBUGGING: Menampilkan lokasi dan isi folder ---
BASE_DIR = os.getcwd()  # Menggunakan getcwd() untuk melihat root direktori
files = os.listdir(BASE_DIR)
st.write(f"Lokasi Kerja: {BASE_DIR}")
st.write(f"File yang terbaca di sistem: {files}")

# --- LOAD DATA ---
FILE_NAME = 'template_coords.json'

if FILE_NAME in files:
    with open(FILE_NAME, 'r') as f:
        KOORDINAT = json.load(f)
    st.success("File JSON ditemukan dan berhasil dimuat!")
else:
    st.error(f"Gagal! File {FILE_NAME} tidak ditemukan. Pastikan file di-upload ke root GitHub!")
    st.stop()

# --- SISA KODE DETEKSI (Sama seperti sebelumnya) ---
def proses_gambar(image):
    file_bytes = np.asarray(bytearray(image.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, 1)
    hasil_jawaban = {}
    
    for no, pilihan in KOORDINAT.items():
        jawaban_terpilih = "-"
        max_density = 0
        for opsi, (x, y) in pilihan.items():
            roi = img[y-15:y+15, x-15:x+15]
            gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
            _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
            kepadatan = cv2.countNonZero(thresh) / thresh.size
            if kepadatan > 0.3 and kepadatan > max_density:
                max_density = kepadatan
                jawaban_terpilih = opsi
        hasil_jawaban[no] = jawaban_terpilih
    return hasil_jawaban

uploaded_file = st.file_uploader("Upload Foto LJK", type=['jpg', 'png', 'jpeg'])
if uploaded_file:
    if st.button("Mulai Koreksi"):
        hasil = proses_gambar(uploaded_file)
        st.write(hasil)
