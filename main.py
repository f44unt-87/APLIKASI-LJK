import streamlit as st
import cv2
import numpy as np

st.title("Koreksi LJK Stabil")

uploaded_file = st.file_uploader("Upload Foto LJK", type=["jpg", "png", "jpeg"])

if uploaded_file:
    # 1. Decode gambar
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, 1)
    
    # 2. Resize agar ukuran seragam (kunci agar tidak error)
    img = cv2.resize(img, (800, 1000))
    
    # 3. Deteksi Lingkaran (HoughCircles) yang lebih sensitif
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # blur sedikit untuk menghilangkan noise
    gray = cv2.medianBlur(gray, 5)
    
    # Gunakan deteksi lingkaran dengan parameter yang disesuaikan untuk LJK Anda
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, dp=1, minDist=20,
                               param1=50, param2=30, minRadius=10, maxRadius=25)
    
    vis = img.copy()
    if circles is not None:
        circles = np.uint16(np.around(circles))
        st.write(f"Ditemukan {len(circles[0])} lingkaran.")
        
        # Urutkan lingkaran berdasarkan posisi Y (dari atas ke bawah)
        sorted_circles = sorted(circles[0, :], key=lambda x: x[1])
        
        for i in sorted_circles:
            # Gambar lingkaran merah
            cv2.circle(vis, (i[0], i[1]), i[2], (0, 0, 255), 2)
    else:
        st.warning("Tidak ditemukan lingkaran. Pastikan foto tidak terlalu buram.")
        
    st.image(cv2.cvtColor(vis, cv2.COLOR_BGR2RGB))
