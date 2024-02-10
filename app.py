#Import All the Required Libraries
import streamlit as st
import google.generativeai as genai
from PIL import Image
import os
from dotenv import load_dotenv
load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def get_txt_response(question):
    model = genai.GenerativeModel(model_name = "gemini-pro")
    prompt_parts = [
        question,
    ]
    response= model.generate_content(prompt_parts).text
    return response

def get_gemini_response(image):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([image])
    return response.text

def input_image_bytes(uploaded_file):
    if uploaded_file is not None:
        #Convert the Uploaded File into bytes
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return  image_parts
    else:
        raise FileNotFoundError("No File Uploaded")

# Initialize the Streamlit App
st.set_page_config(page_title="LunarTurbo2.0")
st.header("TURBOGPT")

input_prompt = """
You are an expert in understanding invoices. Please try to answer the question using the information from the uploaded
invoice.
"""
input_text = st.text_input("Search Here", key="input")
submit = st.button("Enter")
upload_image_file = st.file_uploader("Upload Here", type=["jpg", "jpeg", "png"])
if submit:
    response_txt=get_txt_response(input_text)
    
    st.subheader("Response")
    st.write(response_txt)
if upload_image_file is not None:
    image = Image.open(upload_image_file)
    st.image(image, caption = "Uploaded Image", use_column_width=True)
    response_img= get_gemini_response(image)
    st.write(response_img)

    