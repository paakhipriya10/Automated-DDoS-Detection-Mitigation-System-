

import streamlit as st
import pandas as pd
from src.hybrid_detector import hybrid_predict
from src.explainability import explain
from src.response_simulator import respond
from PIL import Image
import os


import serial
import time
# arduino = serial.Serial('COM3', 9600)
# time.sleep(2)
# 🔥 Arduino connection (run only once)
# if "arduino" not in st.session_state:
#     try:
#         st.session_state.arduino = serial.Serial('COM3', 9600)
#         time.sleep(2)
#     except:
#         st.warning("⚠️ Arduino not connected")


# def send_to_arduino(score):
#     # global arduino
#     if score < 0.50:
#         arduino.write(b'0')   # 🟢 Allow
#     elif score < 0.85:
#         arduino.write(b'2')   # 🟡 Rate limit
#     else:
#         arduino.write(b'1')   # 🔴 Block




# 🔗 Blockchain imports
from blockchain_log import add_log, get_chain, verify_chain

st.set_page_config(
    page_title="DDOS Detection with Explainable AI",
    layout="wide"
)

st.title("🚨 DDOS Attack Detection System")
st.markdown("**Hybrid ML + Deep Learning with Explainable AI (XAI)**")

# Load dataset
data = pd.read_csv("dataset/processed/traffic_processed.csv")
# sample = data.iloc[6:7, :-1]
sample = data.iloc[7:8, :-1]

feature_names = sample.columns.tolist()

st.subheader("📥 Traffic Sample")
st.dataframe(sample)

if st.button("Analyze Traffic"):
    # -----------------------------
    # Prediction
    # -----------------------------
    score = hybrid_predict(sample)
    attack = score > 0.5
    # send_to_arduino(score)

    # -----------------------------
    # Explainability
    # -----------------------------
    explanations = explain(sample, feature_names)

    # -----------------------------
    # Response
    # -----------------------------
    response = respond(attack, score)

    # -----------------------------
    # 🔗 ADD BLOCKCHAIN LOG
    # -----------------------------
    result = "Attack" if attack else "Normal"
    add_log(result, score)

    # -----------------------------
    # OUTPUT
    # -----------------------------
    st.subheader("🔍 Detection Result")

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Attack Detected", str(attack))
    with col2:
        st.metric("Confidence Score", round(score, 3))

    if attack:
        st.subheader("🧠 WHY Traffic Was Blocked")
    else:
        st.subheader("🧠 WHY Traffic Was Allowed")

    for r in explanations:
        st.write("•", r)

    st.subheader("⚙️ Automated Response (Simulation)")
    st.json(response)

    # -----------------------------
    # SHAP PLOTS
    # -----------------------------
    if os.path.exists("shap_outputs"):
        st.subheader("📊 Explainable AI Visualizations")

        col1, col2 = st.columns(2)
        with col1:
            st.image(
                Image.open("shap_outputs/shap_bar.png"),
                caption="SHAP Global Feature Importance",
                use_column_width=True
            )
        with col2:
            st.image(
                Image.open("shap_outputs/shap_waterfall.png"),
                caption="SHAP Local Decision Explanation",
                use_column_width=True
            )

    # -----------------------------
    # 🔗 BLOCKCHAIN VISUAL SECTION
    # -----------------------------
    st.markdown("### 🔐 Secure Logging Layer")

    chain = get_chain()

    if not chain:
        st.info("No logs available yet")
    else:
        st.subheader("🔗 Blockchain Log (Last 5 Entries)")

        for block in reversed(chain[-5:]):

            color = "#ff4d4d" if block["prediction"] == "Attack" else "#4CAF50"

            st.markdown(f"""
            <div style="
                border:2px solid {color};
                padding:12px;
                border-radius:10px;
                margin-bottom:10px;
                background-color:#111;
                color:white;
            ">
                <b>⏱ Time:</b> {block['timestamp']} <br>
                <b>🚨 Prediction:</b> {block['prediction']} <br>
                <b>🔢 Score:</b> {block['score']} <br>
                <b>🔑 Hash:</b> {block['hash'][:25]}... <br>
                <b>↩ Prev Hash:</b> {block['prev_hash'][:25]}...
            </div>
            """, unsafe_allow_html=True)

    # -----------------------------
    # 🔐 INTEGRITY CHECK
    # -----------------------------
    if verify_chain():
        st.success("✅ Blockchain Integrity Verified")
    else:
        st.error("❌ Blockchain Tampered!")





























