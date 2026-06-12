import pandas as pd

from src.hybrid_detector import hybrid_predict
from src.explainability import explain
from src.response_simulator import respond

# 🔗 Import blockchain functions
from blockchain_log import add_log, verify_chain, get_chain

import serial
import time

arduino = serial.Serial('COM3', 9600)
time.sleep(2)

def send_to_arduino(score):
    if score < 0.50:
        arduino.write(b'0')   #  Allow
    elif score < 0.85:
        arduino.write(b'2')   #  Rate limit
    else:
        arduino.write(b'1')   #  Block
    arduino.close()
    


# -----------------------------
# LOAD SAMPLE
# -----------------------------
# sample = pd.read_csv("dataset/processed/traffic_processed.csv").iloc[6:7, :-1]
# sample = pd.read_csv("dataset/processed/traffic_processed.csv").iloc[9:10, :-1]

sample = pd.read_csv("dataset/processed/traffic_processed.csv").iloc[7:8, :-1]
# sample = pd.read_csv("dataset/captured/final_dataset_scaled.csv").iloc[1:2, :-1]
# sample = pd.read_csv("dataset/captured/final_dataset_scaled.csv").iloc[10:11, :-1]


# -----------------------------
# MODEL PREDICTION
# -----------------------------
score = hybrid_predict(sample)
attack = score > 0.5
send_to_arduino(score)

feature_names = sample.columns.tolist()


# -----------------------------
# EXPLAINABILITY
# -----------------------------
explanation = explain(sample, feature_names)


# -----------------------------
# RESPONSE
# -----------------------------
response = respond(attack, score)


# -----------------------------
# 🔗 ADD BLOCKCHAIN LOG
# -----------------------------
result = "Attack" if attack else "Normal"
block = add_log(result, score)


# -----------------------------
# OUTPUT
# -----------------------------
print("\n🚨 Attack Detected:", attack)
print("🔢 Confidence:", round(score, 3))

if attack:
    print("\n🧠 WHY traffic was blocked:")
else:
    print("\n🧠 WHY traffic was allowed:")

for r in explanation:
    print("-", r)

print("\n⚙️ Action:", response)
print("\n📊 SHAP plots saved in 'shap_outputs/' folder")


# -----------------------------
# 🔗 SHOW BLOCKCHAIN LOGS
# -----------------------------
print("\n🔗 BLOCKCHAIN LOG (Last 5 Entries):\n")

chain = get_chain()

for i, b in enumerate(chain[-5:], start=1):
    print(f"--- Block {i} ---")
    print("Time:", b["timestamp"])
    print("Prediction:", b["prediction"])
    print("Score:", b["score"])
    print("Hash:", b["hash"][:25], "...")
    print("Prev Hash:", b["prev_hash"][:25], "...\n")


# -----------------------------
# 🔐 VERIFY INTEGRITY
# -----------------------------
if verify_chain():
    print("✅ Blockchain Integrity: VERIFIED")
else:
    print("❌ Blockchain Integrity: TAMPERED")

