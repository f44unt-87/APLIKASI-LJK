import streamlit as st
import cv2
import numpy as np
import json
import os

# 1. KONFIGURASI PATH DAN OFFSET
BASE_DIR = os.getcwd()
FILE_PATH = os.path.join(BASE_DIR, 'template_coords.json')

# Offset untuk menggeser titik koordinat agar pas di tengah lingkaran
OFFSET_X = -60  
OFFSET_Y = -40  

# 2. LOAD DATA KOORDINAT
if not os.path.exists(FILE_PATH):
    st.error(f"File {FILE_PATH} tidak ditemukan. Pastikan sudah di-upload ke root folder GitHub.")
    st.stop()

with open(FILE_PATH, 'r') as f:
    KOORDINAT = json.load(f)

# 3. FUNGSI PELURUS GAMBAR (WARP PERSPECTIVE)
def luruskan_gambar(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blurred, 75, 200)
    
    contours, _ = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours: return img
    
    kontur_terbesar = max(contours, key=cv2.contourArea)
    peri = cv2.arcLength(kontur_terbesar, True)
    approx = cv2.approxPolyDP(kontur_terbesar, 0.02 * peri, True)
    
    if len(approx) == 4:
        pts = approx.reshape(4, 2)
        rect = np.zeros((4, 2), dtype="float32")
        s = pts.sum(axis=1)
        rect[0] = pts[np.argmin(s)]
        rect[2] = pts[np.argmax(s)]
        diff = np.diff(pts, axis=1)
        rect[1] = pts[np.argmin(diff)]
        rect[3] = pts[np.argmax(diff)]
        
        (tl, tr, br, bl) = rect
        width = max(int(np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))),
                    int(np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))))
        height = max(int(np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))),
                     int(np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))))
        
        dst = np.array([[0, 0], [width - 1, 0], [width - 1, height - 1], [0, height - 1]], dtype="float32")
        M = cv2.getPerspectiveTransform(rect, dst)
        return cv2.warpPerspective(img, M, (width, height))
    return img

# 4. FUNGSI DETEKSI DAN VISUALISASI
def proses_gambar(image):
    file_bytes = np.asarray(bytearray(image.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, 1)
    img_warped = luruskan_gambar(img)
    img_visual = img_warped.copy()
    hasil_jawaban = {}
    
    for no, pilihan in KOORDINAT.items():
        jawaban_terpilih = "-"
        max_density = 0
        
        for opsi, (x_raw, y_raw) in pilihan.items():
            # Terapkan offset
            x = x_raw + OFFSET_X
            y = y_raw + OFFSET_Y
            
            # Area deteksi 25px
            roi = img_warped[y-25:y+25, x-25:x+25]
            if roi.size == 0: continue
            
            gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
            _, thresh = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY_INV)
            kepadatan = cv2.countNonZero(thresh) / thresh.size
            
            # Gambar lingkaran merah untuk panduan kalibrasi
            cv2.circle(img_visual, (x, y), 15, (0, 0, 255), 2)
            
            # Deteksi jawaban
            if kepadatan > 0.20 and kepadatan > max_density:
                max_density = kepadatan
                jawaban_terpilih = opsi
        
        hasil_jawaban[no] = jawaban_terpilih
    
    return hasil_jawaban, img_visual

# 5. UI STREAMLIT
st.title("Koreksi LJK Maslakul Huda")
uploaded_file = st.file_uploader("Upload Foto LJK", type=['jpg', 'png', 'jpeg'])

if uploaded_file:
    st.image(uploaded_file, caption='Foto LJK yang diunggah')
    if st.button("Mulai Koreksi"):
        try:
            hasil, img_visual = proses_gambar(uploaded_file)
            st.success("Hasil Koreksi:")
            st.json(hasil)
            st.subheader("Visualisasi Koordinat ⭕️")
            st.image(cv2.cvtColor(img_visual, cv2.COLOR_BGR2RGB), caption='Peta Koordinat (Merah)', use_column_width=True)
        except Exception as e:
            st.error(f"Gagal memproses gambar: {e}")
