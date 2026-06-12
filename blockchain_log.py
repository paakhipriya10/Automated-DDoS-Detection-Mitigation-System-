import hashlib
import json
import os
from datetime import datetime

# -----------------------------
# LOAD EXISTING BLOCKCHAIN
# -----------------------------
if os.path.exists("blockchain_log.json"):
    with open("blockchain_log.json", "r") as f:
        blockchain = json.load(f)
else:
    blockchain = []

# -----------------------------
# HASH FUNCTION
# -----------------------------
def create_hash(data):
    return hashlib.sha256(data.encode()).hexdigest()

# -----------------------------
# ADD BLOCK
# -----------------------------
def add_log(prediction, score):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    prev_hash = blockchain[-1]["hash"] if blockchain else "0"

    data = timestamp + prediction + str(score) + prev_hash
    current_hash = create_hash(data)

    block = {
        "timestamp": timestamp,
        "prediction": prediction,
        "score": round(score, 3),
        "prev_hash": prev_hash,
        "hash": current_hash
    }

    blockchain.append(block)

    # 💾 SAVE TO FILE
    with open("blockchain_log.json", "w") as f:
        json.dump(blockchain, f, indent=4)

    return block

# -----------------------------
# VERIFY CHAIN
# -----------------------------
def verify_chain():
    for i in range(1, len(blockchain)):
        if blockchain[i]["prev_hash"] != blockchain[i-1]["hash"]:
            return False
    return True

# -----------------------------
# GET FULL CHAIN
# -----------------------------
def get_chain():
    return blockchain