import streamlit as st
import pandas as pd
import joblib
import json
import os

# Load model, pipeline, expected columns, threshold
model      = joblib.load("LightGBM_model.pkl")
pipeline_tuple = joblib.load("pipeline_lightgbm.pkl")
preprocessor   = pipeline_tuple[0]
with open("expected_columns.json") as f:
    expected_columns = json.load(f)
with open("optimal_threshold.json") as f:
    threshold = json.load(f)

st.title("Dropout Prediction - Jaya Jaya Institut")

uploaded_file = st.sidebar.file_uploader("Upload CSV", type="csv")
if uploaded_file is not None:
    # Baca file (cek delimiter kalau perlu)
    df = pd.read_csv(uploaded_file, sep=";")  
    df.columns = df.columns.str.strip()  # Trim spasi

    # --- 1. Feature Engineering Ulang ---
    df['Total_approved_units']    = df['Curricular_units_1st_sem_approved']  + df['Curricular_units_2nd_sem_approved']
    df['Total_units_enrolled']    = df['Curricular_units_1st_sem_enrolled']  + df['Curricular_units_2nd_sem_enrolled']
    df['Avg_grade_all_sem']       = (df['Curricular_units_1st_sem_grade'] + df['Curricular_units_2nd_sem_grade']) / 2
    df['Approval_rate']           = df['Total_approved_units'] / (df['Total_units_enrolled'] + 1e-5)
    df['Financial_stress_index']  = df['Debtor'] + (1 - df['Tuition_fees_up_to_date']) + (1 - df['Scholarship_holder'])
    df['Parental_education_score']= df['Fathers_qualification'] + df['Mothers_qualification']
    df['Parental_status_match']   = ((df['Fathers_occupation'] == df['Mothers_occupation']).astype(int)
                                     + (df['Fathers_qualification'] == df['Mothers_qualification']).astype(int))
    df['Is_adult']                = (df['Age_at_enrollment'] >= 18).astype(int)
    df['Application_effort_index']= df['Application_order'] + df['Application_mode']
    # — selesai feature engineering — 

    # Cek kolom sebelum transform
    missing = set(expected_columns) - set(df.columns)
    if missing:
        st.error(f"Missing columns after feature‑engineering: {missing}")
        st.stop()

    # Urutkan kolom sesuai expected_columns
    df = df[expected_columns]

    # 2. Preprocess & Predict
    X_prep    = preprocessor.transform(df)
    proba     = model.predict_proba(X_prep)[:,1]
    pred      = (proba >= threshold['threshold']).astype(int)

    # Tampilkan hasil
    df['Dropout_Probability'] = proba
    df['Predicted_Dropout']   = pred
    st.write(df[['Predicted_Dropout','Dropout_Probability']])

    st.subheader("Distribusi Probabilitas Dropout")
    st.line_chart(proba)

else:
    st.info("Silakan upload CSV dengan kolom mentah untuk prediksi.")
