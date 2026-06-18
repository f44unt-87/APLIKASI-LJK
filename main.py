import streamlit as st
import cv2
import numpy as np
from streamlit_drawable_canvas import st_canvas # Perlu instal: pip install streamlit-drawable-canvas

st.title("Kalibrasi LJK Otomatis")

# 1. Upload Foto LJK Kosong
uploaded_file = st.file_uploader("Upload LJK Kosong untuk Kalibrasi", type=["jpg", "png"])

if uploaded_file:
    img = cv2.imdecode(np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8), 1)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # 2. Canvas untuk klik titik referensi
    st.write("Klik pada titik 1A, 1E, 50A, dan 50E")
    canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",
        stroke_width=2,
        stroke_color="#E91E63",
        background_image=img,
        height=img.shape[0],
        width=img.shape[1],
        drawing_mode="point",
        key="canvas",
    )

    if canvas_result.json_data is not None:
        objs = canvas_result.json_data["objects"]
        if len(objs) >= 4:
            st.success("Titik berhasil disimpan! Sistem akan menghitung posisi semua lingkaran.")
            # Di sini sistem akan menyimpan koordinat (x, y) dari 4 titik klik Anda
            # dan menghitung posisi sisanya secara matematis (Interpolasi Linear).
