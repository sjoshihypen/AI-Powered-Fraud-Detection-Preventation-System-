import streamlit as st
import cv2
import face_recognition
#import deepface
import numpy as np
from PIL import Image
from transformers import pipeline

# Set up Streamlit page
st.title('Identity Verification & Fraud Prevention Module')

# Upload an identity document
uploaded_file = st.file_uploader("Upload Identity Document (Image)", type=['jpg', 'jpeg', 'png'])

# Upload an image for face verification
uploaded_face = st.file_uploader("Upload Face Image for Verification", type=['jpg', 'jpeg', 'png'])

# Input name for NLP-based verification
name_input = st.text_input("Enter the name as per the ID document")

# Function for image verification (face comparison)
def verify_face(doc_img, face_img):
    # Load and encode the images using face_recognition
    doc_image = face_recognition.load_image_file(doc_img)
    face_image = face_recognition.load_image_file(face_img)
    # doc_image = deepface.load_image_file(doc_img)
    # face_image = deepface.load_image_file(face_img)
    try:
        doc_encoding = face_recognition.face_encodings(doc_image)[0]
        face_encoding = face_recognition.face_encodings(face_image)[0]
        # doc_encoding = deepface.face_encodings(doc_image)[0]
        # face_encoding = deepface.face_encodings(face_image)[0]
        
        # Compare faces
        results = face_recognition.compare_faces([doc_encoding], face_encoding)
        # results = deepface.compare_faces([doc_encoding], face_encoding)
        return results[0]
    except IndexError:
        return None  # No face detected

# Function for name verification using NLP
def verify_name(name_in_id, user_name):
    # Load a pre-trained name matching model
    name_matching = pipeline("fill-mask", model="bert-base-uncased")
    
    # Check similarity
    mask_text = f"{name_in_id} is a [MASK]"
    output = name_matching(mask_text)
    
    predicted_name = output[0]['token_str'].strip().lower()
    return predicted_name == user_name.lower()

# Display verification results
if uploaded_file and uploaded_face and name_input:
    st.write("Verifying Identity...")
    
    # Document Verification
    document_image = Image.open(uploaded_file)
    face_image = Image.open(uploaded_face)
    
    # Verify face
    face_verified = verify_face(uploaded_file, uploaded_face)
    
    # NLP-based name verification
    name_verified = verify_name(name_input, name_input)
    
    # Generate risk score
    fraud_risk = np.random.randint(1, 101)  # Simulated risk score
    
    if face_verified and name_verified:
        st.success(f"Identity Verified! Fraud Risk Score: {fraud_risk}/100")
    else:
        st.error(f"Identity Verification Failed. Fraud Risk Score: {fraud_risk}/100")
else:
    st.write("Please upload both images and provide a name for verification.")

