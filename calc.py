import streamlit as st
import pandas as pd
from rasar_desc import rasar_desc_calculation
import io

# --- Page Config ---
st.set_page_config(page_title="RASAR", layout="wide")


st.title("📊 RASAR Descriptor Calculation")

# --- Dropdown for calculation type ---
calc_type = st.selectbox(
    "Select Type of Calculation",
    ["User defined descriptors", "Selected RDKit descriptors", "All RDKit descriptors"]
)

# --- Two columns for train & test side by side ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("📘 Training Set")
    train_file = st.file_uploader("Upload Training Set (.xlsx)", type=["xlsx"], key="train")

with col2:
    st.subheader("📗 Test Set")
    test_file = st.file_uploader("Upload Test Set (.xlsx)", type=["xlsx"], key="test")

# --- Function to read Excel ---
def load_excel(uploaded_file):
    if uploaded_file is not None:
        return pd.read_excel(uploaded_file, index_col=0)
    return None

train_df = load_excel(train_file)
test_df = load_excel(test_file)

# --- Show previews side by side ---
if train_df is not None and test_df is not None:
    col1, col2 = st.columns(2)

    with col1:
        st.write(" ")
        st.dataframe(train_df)

    with col2:
        st.write(" ")
        st.dataframe(test_df)

# --- Example ML operation (dummy - replace with real one) ---
if train_df is not None and test_df is not None:
    st.subheader("⚙️ Running Operation...")
    st.write(f"Calculation Type Selected: **{calc_type}**")

    
    tr_rasar_desc = rasar_desc_calculation(df5=train_df, df6=train_df, des=calc_type)
    te_rasar_desc = rasar_desc_calculation(df5=train_df, df6=test_df, des=calc_type) 

    st.subheader("📤 Generated Outputs")
    col3, col4 = st.columns(2)
    
    with col3:
        st.write("Training RASAR Descriptors")
        st.dataframe(tr_rasar_desc)

    with col4:
        st.write("Test RASAR Descriptors")
        st.dataframe(te_rasar_desc)

  
