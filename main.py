import streamlit as st
import cv2
import numpy as np
from streamlit_drawable_canvas import st_canvas
from PIL import Image

st.title("Kalibrasi Titik Manual")

uploaded_file = st.file_uploader("Upload Foto LJK", type=["jpg", "png"])

if uploaded_file:
    img = cv2.imdecode(np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8), 1)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(img_rgb)
    
    st.write("Klik pada lingkaran 1A, 1E, dan 50E untuk melihat koordinatnya:")
    
    canvas = st_canvas(
        background_image=pil_image,
        width=pil_image.width,
        height=pil_image.height,
        drawing_mode="point",
        key="canvas",
    )

    if canvas.json_data is not None:
        for obj in canvas.json_data["objects"]:
            x, y = obj["left"], obj["top"]
            st.write(f"Koordinat ditemukan: x={int(x)}, y={int(y)}")
