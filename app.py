import streamlit as st
import pandas as pd
import joblib
import gdown
import os

# =========================
# DOWNLOAD MODEL (GOOGLE DRIVE)
# =========================
if not os.path.exists("model.pkl"):
    url = "https://drive.google.com/uc?id=1Q3uuF56D_VGRE7tNG9NLydtNEBWZDUw5"
    gdown.download(url, "model.pkl", quiet=False)

# =========================
# LOAD MODEL
# =========================
model = joblib.load("model.pkl")

st.title("Deteksi Potensi Fraud")
st.write("Masukkan data transaksi:")

# =========================
# INPUT USER
# =========================
step = st.number_input("Step", min_value=0)
type_val = st.selectbox("Type", ["CASH_OUT", "PAYMENT", "TRANSFER"])
amount = st.number_input("Amount", min_value=0.0)
oldbalanceOrg = st.number_input("Old Balance Org", min_value=0.0)
newbalanceOrig = st.number_input("New Balance Orig", min_value=0.0)
oldbalanceDest = st.number_input("Old Balance Dest", min_value=0.0)
newbalanceDest = st.number_input("New Balance Dest", min_value=0.0)
isFlaggedFraud = st.selectbox("Flagged Fraud", [0,1])

# =========================
# ENCODING TYPE → CLASS
# =========================
type_map = {
    "CASH_OUT": 0,
    "PAYMENT": 1,
    "TRANSFER": 2
}

type_encoded = type_map[type_val]

# =========================
# PREDIKSI
# =========================
if st.button("Prediksi"):

    data = [[
        step,
        type_encoded,  # masuk ke Class
        amount,
        oldbalanceOrg,
        newbalanceOrig,
        oldbalanceDest,
        newbalanceDest,
        isFlaggedFraud
    ]]

    # 🔥 FIX DI SINI (type → Class)
    columns = [
        'step','Class','amount','oldbalanceOrg',
        'newbalanceOrig','oldbalanceDest',
        'newbalanceDest','isFlaggedFraud'
    ]

    df = pd.DataFrame(data, columns=columns)

    pred = model.predict(df)

    label_map = {
        0: "CASH_OUT",
        1: "PAYMENT",
        2: "TRANSFER"
    }

    hasil = label_map[pred[0]]

    st.success(f"Jenis Transaksi: {hasil}")

    # =========================
    # INTERPRETASI FRAUD
    # =========================
    if hasil in ["TRANSFER", "CASH_OUT"]:
        st.error("⚠️ Berpotensi Fraud")
    else:
        st.success("Aman")