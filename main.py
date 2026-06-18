import streamlit as st
import cv2
import numpy as np

st.title("Deteksi Lingkaran Otomatis (Tanpa Koordinat)")

up = st.file_uploader("Upload Foto LJK", type=['jpg', 'png'])

if up and st.button("Proses Otomatis"):
    file_bytes = np.asarray(bytearray(up.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, 1)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Deteksi lingkaran menggunakan HoughCircles
    # Ini akan mencari semua bentuk lingkaran di kertas secara otomatis
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, dp=1.2, minDist=20,
                               param1=50, param2=30, minRadius=5, maxRadius=20)
    
    vis = img.copy()
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            # Gambar lingkaran merah pada setiap lingkaran yang ditemukan
            cv2.circle(vis, (i[0], i[1]), i[2], (0, 0, 255), 2)
            
    st.image(cv2.cvtColor(vis, cv2.COLOR_BGR2RGB), use_column_width=True)
    st.write(f"Ditemukan {len(circles[0])} lingkaran.")
