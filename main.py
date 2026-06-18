import streamlit as st
import cv2
import numpy as np
from imutils.perspective import four_point_transform # Pastikan install imutils

def process_ljk(image):
    # 1. Konversi ke grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # 2. Deteksi tepi kertas
    edged = cv2.Canny(blurred, 75, 200)
    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    
    if len(cnts) > 0:
        c = max(cnts, key=cv2.contourArea)
        # 3. Transformasi perspektif (ini kunci agar posisi selalu pas)
        warped = four_point_transform(image, c.reshape(4, 2))
        return warped
    return image

# Di bagian utama Streamlit:
uploaded_file = st.file_uploader("Upload LJK")
if uploaded_file:
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, 1)
    
    # Panggil fungsi pelurusan yang stabil
    img_fixed = process_ljk(img)
    
    st.image(cv2.cvtColor(img_fixed, cv2.COLOR_BGR2RGB))
