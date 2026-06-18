import streamlit as st
import cv2
import numpy as np
import base64
from io import BytesIO
from streamlit_drawable_canvas import st_canvas
from PIL import Image

st.title("Kalibrasi LJK Presisi")

uploaded_file = st.file_uploader("Upload Foto LJK Kosong", type=["jpg", "png", "jpeg"])

if uploaded_file:
    # Load gambar
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, 1)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(img_rgb)
    
    # --- KONVERSI KE BASE64 (MENGHINDARI ERROR URL) ---
    buffered = BytesIO()
    pil_image.save(buffered, format="PNG")
    img_base64 = base64.b64encode(buffered.getvalue()).decode()
    img_url = f"data:image/png;base64,{img_base64}"
    # --------------------------------------------------
    
    st.write("### 1. Klik pada titik 1A, 1E, 50A, dan 50E")
    
    # Gunakan background_image_url dengan data base64
    canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",
        stroke_width=3,
        stroke_color="#FF0000",
        background_image_url=img_url, # Menggunakan URL base64
        height=pil_image.height,
        width=pil_image.width,
        drawing_mode="point",
        key="canvas",
    )

    if canvas_result.json_data is not None:
        objs = canvas_result.json_data["objects"]
        if len(objs) >= 4:
            st.success("Titik berhasil disimpan!")
