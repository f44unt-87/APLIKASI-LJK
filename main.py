import streamlit as st
import cv2
import numpy as np
import json
import os

# 1. KONFIGURASI PATH
BASE_DIR = os.getcwd()
FILE_PATH = os.path.join(BASE_DIR, 'template_coords.json')

# 2. LOAD KOORDINAT (Gunakan template JSON Anda yang asli)
with open(FILE_PATH, 'r') as f:
    KOORDINAT = json.load(f)

# 3. FUNGSI PELURUS GAMBAR (WARP PERSPECTIVE)
def luruskan_ljk(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blurred, 75, 200)
    
    contours, _ = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours: return img
    
    # Ambil kontur terbesar (kertas)
    kontur = max(contours, key=cv2.contourArea)
    peri = cv2.arcLength(kontur, True)
    approx = cv2.approxPolyDP(kontur, 0.02 * peri, True)
    
    if len(approx) == 4:
        pts = approx.reshape(4, 2)
        # Urutkan titik sudut
        rect = np.zeros((4, 2), dtype="float32")
        s = pts.sum(axis=1)
        rect[0] = pts[np.argmin(s)] # top-left
        rect[2] = pts[np.argmax(s)] # bottom-right
        diff = np.diff(pts, axis=1)
        rect[1] = pts[np.argmin(diff)] # top-right
        rect[3] = pts[np.argmax(diff)] # bottom-left
        
        # --- PERBAIKAN: GUNAKAN UKURAN TETAP ---
        # Gunakan ukuran canvas yang sama dengan ukuran JSON Anda
        # Misalkan canvas JSON Anda adalah 800x1000. Ganti angka ini jika berbeda.
        w, h = 800, 1000 
        dst = np.array([[0,0], [w-1,0], [w-1,h-1], [0,h-1]], dtype="float32")
        M = cv2.getPerspectiveTransform(rect, dst)
        return cv2.warpPerspective(img, M, (w, h))
    return img

# 4. PROSES DETEKSI
def proses_ljk(image_file):
    file_bytes = np.asarray(bytearray(image_file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, 1)
    
    # Pelurusan gambar dengan ukuran canvas JSON yang tetap
    img_warped = luruskan_ljk(img)
    vis = img_warped.copy()
    hasil = {}
    
    for no, pilihan in KOORDINAT.items():
        hasil[no] = "-"
        max_d = 0
        # Paksa 5 pilihan A, B, C, D, E
        for opt in ['A', 'B', 'C', 'D', 'E']:
            if opt not in pilihan: continue
            
            x, y = pilihan[opt]
            # Lingkaran panduan visual untuk melihat seberapa pas
            cv2.circle(vis, (int(x), int(y)), 15, (0, 0, 255), 2)
            
            roi = img_warped[int(y)-15:int(y)+15, int(x)-15:int(x)+15]
            if roi.size == 0: continue
            
            gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
            _, thresh = cv2.threshold(gray_roi, 120, 255, cv2.THRESH_BINARY_INV)
            d = cv2.countNonZero(thresh) / thresh.size
            
            if d > 0.15 and d > max_d: # sensitivitas
                max_d = d
                hasil[no] = opt
                
    return hasil, vis

# 5. UI
st.title("Sistem Koreksi LJK Maslakul Huda")
up = st.file_uploader("Upload LJK", type=['jpg', 'png'])
if up and st.button("Proses Koreksi"):
    res, vis = proses_ljk(up)
    st.subheader("Hasil JSON:")
    st.json(res)
    st.subheader("Visualisasi Koordinat ⭕️")
    st.image(cv2.cvtColor(vis, cv2.COLOR_BGR2RGB), caption='Peta Koordinat (Merah)', use_column_width=True)
