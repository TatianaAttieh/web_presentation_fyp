import streamlit as st
import joblib
import numpy as np
 
tfidf = joblib.load("tfidf_vectorizer.pkl")
lr_bin = joblib.load("lr_tfidf_binary.pkl")
lr_multi = joblib.load("lr_tfidf_multiclass.pkl")
le_bin = joblib.load("label_encoder_binary.pkl")
le_multi = joblib.load("label_encoder_multiclass.pkl")
 
st.set_page_config(page_title="🧠Mental Health Classifier", layout="centered")
 
# CSS for full dark theme with white input box and pastel border
st.markdown("""
<style>
html, body, [class*="css"] {
    background-color: #1e1e1e !important;
    color: #f0f0f0 !important;
}
 
/* White text area with pastel border */
textarea {
    background-color: #ffffff !important;
    color: #1a1a1a !important;
    border: 2px solid #a4c2f4 !important;
    border-radius: 8px !important;
    padding: 10px !important;
}
 
/* Pastel info box */
.pastel-box {
    background-color: #f9f9f9 !important;
    color: #333333 !important;
    padding: 1em;
    border-radius: 12px;
    border-left: 6px solid #a4c2f4;
    margin-bottom: 20px;
}
 
/* Confidence note */
.confidence-note {
    font-size: 0.85em;
    color: #555555 !important;
    margin-top: -10px;
    background-color: #f0f0f0 !important;
    padding: 4px 8px;
    border-radius: 6px;
}
 
/* Support message box */
.support-message {
    background-color: #f9f9f9 !important;
    color: #333333 !important;
    padding: 1em;
    border-radius: 10px;
    margin-top: 20px;
    border-left: 6px solid #f4b6c2;
}
 
/* Buttons */
.stButton > button {
    background-color: #a4c2f4 !important;
    color: black !important;
    font-weight: bold;
    border-radius: 8px;
    padding: 0.5em 1em;
}
 
.stButton > button:hover {
    background-color: #d5e3ff !important;
    color: black !important;
}
 
/* Heading darker pastel */
h1 {
    color: #5f54c7 !important;
}
</style>
""", unsafe_allow_html=True)
 
st.markdown("<h1>Mental Health Text Classifier</h1>", unsafe_allow_html=True)
st.markdown("""
<div class='pastel-box'>
    This app classifies your text into one of the following categories:
<ul>
<li>Normal</li>
<li>Anxiety</li>
<li>Depression</li>
<li>Suicidal</li>
</ul>
    It also provides a confidence score when a category is detected.
</div>
""", unsafe_allow_html=True)
 
user_input = st.text_area("Enter your text here:", height=150, placeholder="Type how you're feeling today...")
 
if st.button("Classify"):
    if not user_input.strip():
        st.warning("Please enter some text before clicking classify.")
    else:
        X_input = tfidf.transform([user_input])
        y_bin_pred = lr_bin.predict(X_input)
        label_bin = le_bin.inverse_transform(y_bin_pred)[0]
 
        if label_bin.lower() == "normal":
            st.success("The input is classified as NORMAL.")
        else:
            y_multi_pred = lr_multi.predict(X_input)
            y_multi_proba = lr_multi.predict_proba(X_input)
            label_multi = le_multi.inverse_transform(y_multi_pred)[0]
 
            st.error(f"The input is classified as {label_multi.upper()}.")
 
            # Show confidence percentage for the predicted class
            try:
                class_list = list(le_multi.classes_)
                idx = class_list.index(label_multi)
                confidence = round(y_multi_proba[0][idx] * 100, 2)
                st.info(f"{label_multi.capitalize()} Confidence Score: {confidence}%")
                st.markdown(
                    "<div class='confidence-note'>Note: This score reflects the model's confidence, not the severity of the condition.</div>",
                    unsafe_allow_html=True
                )
            except ValueError:
                pass
 
            if label_multi.lower() in ["anxiety", "depression", "suicidal"]:
                st.markdown("""
<div class='support-message'>
                    If you're feeling down, please consider reaching out to  the National Lifeline .<br>
                    📞 Call <strong>1564</strong> for Emotional Support and Suicide Prevention Hotline.
</div>
                """, unsafe_allow_html=True)
               
