import streamlit as st
import pandas as pd
import requests
from PIL import Image

API_URL = "http://127.0.0.1:8000"  # FastAPI backend

st.set_page_config(page_title="TrendTeller", page_icon="📊", layout="wide")
st.title("📊 TrendTeller - Smart Dataset & Insights Manager")

# ----------------- Upload Dataset -----------------
st.header("📂 Upload a Dataset")
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success("✅ File uploaded successfully!")
    st.dataframe(df.head())

    dataset_name = st.text_input("Dataset Name", value=uploaded_file.name.split(".")[0])
    uploaded_by = st.text_input("Uploaded By", value="Anonymous")

    if st.button("Save Dataset"):
        if dataset_name and uploaded_by and uploaded_file:
            uploaded_file.seek(0)  # Reset pointer before sending
            data = {"name": dataset_name, "uploaded_by": uploaded_by}
            files = {"file": (uploaded_file.name, uploaded_file, "text/csv")}
            response = requests.post(f"{API_URL}/datasets/", data=data, files=files)

            if response.status_code == 200:
                st.success("✅ Dataset saved successfully!")
            else:
                st.error(f"❌ Error: {response.json().get('detail', 'Unknown error')}")
        else:
            st.error("Please fill all fields and upload a file.")

# ----------------- View All Datasets -----------------
st.header("📑 View All Datasets")
if st.button("Load Datasets"):
    response = requests.get(f"{API_URL}/datasets/")
    if response.status_code == 200:
        datasets = response.json()
        if datasets:
            for ds in datasets:
                with st.expander(f"📂 {ds['name']} (ID: {ds['id']})"):
                    st.write(f"👤 Uploaded by: {ds['uploaded_by']}")
                    st.dataframe(pd.DataFrame(ds['data']).head())
        else:
            st.info("No datasets found.")
    else:
        st.error("❌ Failed to fetch datasets.")

# ----------------- Add Insights -----------------
st.header("💡 Add Insight")
dataset_id = st.number_input("Dataset ID", min_value=1, step=1)
summary = st.text_area("Insight Summary (optional, leave empty for auto)")

if st.button("Save Insight"):
    try:
        payload = {"dataset_id": dataset_id}
        if summary.strip():
            payload["summary"] = summary.strip()

        response = requests.post(f"{API_URL}/insights/", json=payload)

        if response.status_code == 200:
            st.success("✅ Insight added successfully!")
        else:
            st.error(f"❌ Failed to add insight: {response.json().get('detail', 'Unknown error')}")
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")

# ----------------- View Insights -----------------
st.header("🔍 View Insights")
insight_dataset_id = st.number_input(
    "Enter Dataset ID to fetch insights", min_value=1, step=1, key="insights_input"
)

if st.button("Get Insights"):
    try:
        response = requests.get(f"{API_URL}/insights/{insight_dataset_id}")
        if response.status_code == 200:
            insights = response.json()
            if insights:
                for ins in insights:
                    with st.expander(f"💡 Insight ID: {ins['id']}"):
                        st.write(f"📌 Summary: {ins['summary']}")
                        # Show plots smaller
                        for plot_file in ins["plots"]:
                            try:
                                image = Image.open(plot_file)
                                image = image.resize((500, 350))  # resized to smaller dimensions
                                st.image(image)
                            except Exception as e:
                                st.error(f"Could not load image {plot_file}: {str(e)}")
            else:
                st.info("No insights found for this dataset.")
        else:
            st.error("❌ Failed to fetch insights.")
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
