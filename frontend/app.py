import streamlit as st
import pandas as pd
import requests
from PIL import Image
import matplotlib.pyplot as plt

API_URL = "http://127.0.0.1:8000"  # FastAPI backend

st.set_page_config(page_title="TrendTeller", page_icon="📊", layout="wide")
st.title("📊 TrendTeller - Data Made Simple")

# ----------------- Sidebar Navigation -----------------
page = st.sidebar.radio("Go To Page:", [
    "Upload Dataset",
    "View Datasets",
    "Add Insight",
    "View Insights"
])

# ----------------- Upload Dataset -----------------
if page == "Upload Dataset":
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
                uploaded_file.seek(0)
                data = {"name": dataset_name, "uploaded_by": uploaded_by}
                files = {"file": (uploaded_file.name, uploaded_file, "text/csv")}
                response = requests.post(f"{API_URL}/datasets/", data=data, files=files)
                if response.status_code == 200:
                    st.success("✅ Dataset saved successfully!")
                else:
                    st.error(f"❌ Error: {response.json().get('detail', 'Unknown error')}")
            else:
                st.error("Please fill all fields and upload a file.")

# ----------------- View Datasets -----------------
elif page == "View Datasets":
    st.header("📑 Datasets")
    response = requests.get(f"{API_URL}/datasets/")
    if response.status_code == 200:
        datasets = response.json()
        if datasets:
            num_columns = 2
            rows = (len(datasets) + num_columns - 1) // num_columns
            for r in range(rows):
                cols = st.columns(num_columns)
                for c in range(num_columns):
                    idx = r * num_columns + c
                    if idx < len(datasets):
                        ds = datasets[idx]
                        with cols[c]:
                            st.subheader(f"📂 {ds['name']} (ID: {ds['id']})")
                            st.write(f"👤 Uploaded by: {ds['uploaded_by']}")
                            st.write(f"📅 Uploaded at: {ds.get('uploaded_at', 'N/A')}")
                            if st.button(f"Show Data {ds['id']}", key=f"data_{ds['id']}"):
                                st.dataframe(pd.DataFrame(ds['data']).head())

# ----------------- Add Insight -----------------
elif page == "Add Insight":
    st.header("💡 Add Insight")

    # Fetch latest dataset ID automatically
    datasets_resp = requests.get(f"{API_URL}/datasets/")
    latest_dataset_id = None
    if datasets_resp.status_code == 200 and datasets_resp.json():
        latest_dataset = datasets_resp.json()[-1]
        latest_dataset_id = latest_dataset['id']
        st.info(f"Using latest dataset: {latest_dataset['name']} (ID: {latest_dataset_id})")

    dataset_id = st.number_input(
        "Dataset ID", min_value=1, step=1,
        value=latest_dataset_id if latest_dataset_id else 1
    )

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
elif page == "View Insights":
    st.header("🔍 View Insights")

    # Fetch latest dataset ID automatically
    datasets_resp = requests.get(f"{API_URL}/datasets/")
    latest_dataset_id = None
    if datasets_resp.status_code == 200 and datasets_resp.json():
        latest_dataset = datasets_resp.json()[-1]
        latest_dataset_id = latest_dataset['id']
        st.info(f"Showing insights for latest dataset: {latest_dataset['name']} (ID: {latest_dataset_id})")

    insight_dataset_id = st.number_input(
        "Dataset ID to fetch insights", min_value=1, step=1,
        value=latest_dataset_id if latest_dataset_id else 1
    )

    if st.button("Get Insights"):
        try:
            response = requests.get(f"{API_URL}/insights/{insight_dataset_id}")
            if response.status_code == 200:
                insights = response.json()
                if insights:
                    dataset_resp = requests.get(f"{API_URL}/datasets/{insight_dataset_id}")
                    if dataset_resp.status_code == 200:
                        df = pd.DataFrame(dataset_resp.json()['data'])
                        df.columns = df.columns.str.strip().str.capitalize()
                        if 'Date' in df.columns:
                            df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

                        for ins in insights:
                            with st.expander(f"💡 Insight ID: {ins['id']}"):
                                # Text summary
                                st.subheader("Insight Summary")
                                st.write(ins['summary'])

                                # Prepare charts if relevant columns exist
                                if 'Category' in df.columns and 'Mentions' in df.columns:
                                    mentions_per_category = df.groupby('Category')['Mentions'].sum().reset_index()
                                    fig1, ax1 = plt.subplots(figsize=(5, 3))
                                    ax1.bar(mentions_per_category['Category'], mentions_per_category['Mentions'], color='skyblue')
                                    ax1.set_ylabel("Total Mentions")
                                    ax1.set_title("Total Mentions by Category")
                                    fig1.tight_layout()

                                if 'Date' in df.columns and 'Category' in df.columns and 'Mentions' in df.columns:
                                    fig2, ax2 = plt.subplots(figsize=(5, 3))
                                    for category in df['Category'].unique():
                                        subset = df[df['Category'] == category]
                                        ax2.plot(subset['Date'], subset['Mentions'], marker='o', label=category)
                                    ax2.set_xlabel("Date")
                                    ax2.set_ylabel("Mentions")
                                    ax2.set_title("Trend of Mentions Over Time")
                                    ax2.legend()
                                    fig2.tight_layout()

                                # Display charts side by side
                                col1, col2 = st.columns(2)
                                with col1:
                                    if 'Category' in df.columns and 'Mentions' in df.columns:
                                        st.pyplot(fig1, use_container_width=True)
                                with col2:
                                    if 'Date' in df.columns and 'Category' in df.columns and 'Mentions' in df.columns:
                                        st.pyplot(fig2, use_container_width=True)

                    else:
                        st.error("❌ Could not fetch dataset for charts")
                else:
                    st.info("No insights found for this dataset.")
            else:
                st.error("❌ Failed to fetch insights.")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
