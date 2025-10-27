import streamlit as st
import pandas as pd
from rasar_desc import rasar_desc_calculation
import io

# --- Page Config ---
st.set_page_config(page_title="RASAR", layout="wide")

# --- Title ---
st.title("📊 RASAR Descriptor Calculation")

# --- Sidebar ---
st.sidebar.header("⚙️ Controls")

calc_type = st.sidebar.selectbox(
    "Select Type of Calculation",
    ["User defined descriptors", "Selected RDKit descriptors", "All RDKit descriptors"]
)

run_button = st.sidebar.button("🚀 Run")

st.sidebar.markdown("---")
st.sidebar.markdown("**About:** This app calculates RASAR descriptors for training and test datasets based on the Gaussian Kernel similarity function.")


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
        st.markdown("#### Uploaded Training Set")
        st.dataframe(train_df)

    with col2:
        st.markdown("#### Uploaded Test Set")
        st.dataframe(test_df)


# --- Run calculation when button clicked ---
if run_button:
    if train_df is not None and test_df is not None:
        with st.spinner("🧮 Calculating RASAR Descriptors... Please wait."):
            tr_rasar_desc = rasar_desc_calculation(df5=train_df, df6=train_df, des=calc_type)
            te_rasar_desc = rasar_desc_calculation(df5=train_df, df6=test_df, des=calc_type)

        st.success("✅ Calculation Completed Successfully!")

        st.subheader("📤 Generated Outputs")
        col3, col4 = st.columns(2)
        
        with col3:
            st.write("Training RASAR Descriptors")
            st.dataframe(tr_rasar_desc)

        with col4:
            st.write("Test RASAR Descriptors")
            st.dataframe(te_rasar_desc)

        # --- Export button ---
        tr_rasar_desc_df  = pd.DataFrame(tr_rasar_desc, index=train_df.index)
        te_rasar_desc_df  = pd.DataFrame(te_rasar_desc, index=test_df.index)
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            tr_rasar_desc_df.to_excel(writer, sheet_name="Training_RASAR")
            te_rasar_desc_df.to_excel(writer, sheet_name="Test_RASAR")
        excel_data = output.getvalue()

        st.download_button(
            label="💾 Export Results as Excel",
            data=excel_data,
            file_name="RASAR_descriptors.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.warning("⚠️ Please upload both Training and Test files before running the calculation.")


# --- Footer ---
st.markdown("---")
footer_col1, footer_col2, footer_col3 = st.columns(3)

with footer_col1:
    st.markdown("### 🔗 Quick Links")
    st.markdown("- [📘 User Manual](https://drive.google.com/file/d/1cqJsBO1WFHcLqVY6lk11rh-3dbixum73/view?usp=sharing)")
    st.markdown("- [📂 Sample Files](https://drive.google.com/drive/folders/1p4oojID_rIfK0kaxvSMfgmcSbs7YxqFU?usp=sharing)")
    st.markdown("- [🧠 Other Tools](https://sites.google.com/jadavpuruniversity.in/dtc-lab-software/home)")

with footer_col2:
    st.markdown("### 📬 Contact")
    st.markdown("kunal.roy@\u200bjadavpuruniversity.in")
    st.markdown("souvikpore123@\u200bgmail.com")

with footer_col3:
    st.markdown("### 📚 References")
    st.markdown("- [Banerjee & Roy, Mol. Divers.](https://doi.org/10.1007/s11030-022-10478-6)")
    st.markdown("- [Banerjee & Roy, Chem. Res. Toxicol.](https://doi.org/10.1021/acs.chemrestox.2c00374)")
    st.markdown("- [Banerjee & Roy, Chem. Res. Toxicol.](https://doi.org/10.1021/acs.chemrestox.3c00155)")

