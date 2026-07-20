import os
import streamlit as st
import requests
import base64

API_URL = os.getenv("API_URL", "http://127.0.0.1:4444")

test_images = requests.get(f"{API_URL}/preload").json()


st.title("Segmentation sémantique embarquée — Véhicule autonome")
st.caption("Dataset : Cityscapes (8 classes agrégées) · Modèle : MobileNetV3Small-UNet (fine-tuning)")

# selected = st.selectbox("Select a image", options=test_images, format_func=lambda x: x["path"])
selected = st.selectbox("Select a image", options=test_images, format_func=lambda x: x["path"].split("/")[-1])

response = requests.post(f"{API_URL}/select_img", json={"image_index": selected["index"]})

image_orig = base64.b64decode(response.json()["image"])
mask = base64.b64decode(response.json()["mask"])

col1, col2 = st.columns(2)
with col1:
    st.image(image_orig)
with col2:
    st.image(mask)


col1, col2, col3 = st.columns([2,1,2])

with col2:
    st.markdown("""
                    <style>
                    div.stButton > button {
                        background-color: red;
                        color: white;
                        border: none;
                    }
                    div.stButton > button:hover {
                        background-color: darkred;
                        color: white;
                    }
                    </style>
                """, unsafe_allow_html=True)

    gros_bouton = st.button("§ PREDICT §")


col1, col2, col3 = st.columns([1,3,1])
with col2:
    if gros_bouton:
        response = requests.post(f"{API_URL}/predict", json={"image_index": selected["index"]})
        mask_pred = base64.b64decode(response.json()["img_mask_pred"])
        st.caption("Modèle : MobileNetV3Small-UNet · val Dice = 0.696 · val mIoU = 0.661")
        st.image(mask_pred)
