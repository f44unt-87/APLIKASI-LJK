import streamlit as st
import cv2
import numpy as np
from streamlit_drawable_canvas import st_canvas
from PIL import Image # Tambahkan import ini

st.title("Kalibrasi LJK Presisi")

uploaded_file = st.file_uploader("Upload Foto LJK Kosong", type=["jpg", "png", "jpeg"])

if uploaded_file:
    # 1. Load gambar dengan OpenCV
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, 1)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # 2. KONVERSI KE PIL IMAGE (Ini yang memperbaiki error)
    pil_image = Image.fromarray(img_rgb)
    
    st.write("### 1. Klik pada titik 1A, 1E, 50A, dan 50E")
    
    # 3. Gunakan pil_image di background_image
    canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",
        stroke_width=3,
        stroke_color="#FF0000",
        background_image=pil_image, # Ganti jadi pil_image
        height=pil_image.height,
        width=pil_image.width,
        drawing_mode="point",
        key="canvas",
    )

    if canvas_result.json_data is not None:
        objs = canvas_result.json_data["objects"]
        if len(objs) >= 4:
            st.success("Titik berhasil disimpan!")
