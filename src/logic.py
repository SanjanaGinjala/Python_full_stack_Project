from src.supabase_db import supabase
import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime
import json

# ---------------- Dataset Manager ----------------
class DatasetManager:
    def __init__(self):
        self._datasets = {}  # Local cache

    def add_dataset(self, name, uploaded_by, data_json):
        """Add dataset to Supabase and local cache."""
        # Convert data to JSON if it's a DataFrame or list of dicts
        if isinstance(data_json, pd.DataFrame):
            data_json_str = data_json.to_dict(orient="records")
        elif isinstance(data_json, list):
            data_json_str = data_json
        else:
            data_json_str = data_json  # assume already JSON

        # Insert dataset into Supabase (id auto-generated)
        response = supabase.table("datasets").insert({
            "name": name,
            "uploaded_by": uploaded_by,
            "data": data_json_str,
            "uploaded_at": datetime.utcnow().isoformat()
        }).execute()

        print("🧩 Supabase insert response:", response)

        # Get the id assigned by Supabase
        if response.data and len(response.data) > 0:
            dataset_id = response.data[0]["id"]  # Supabase-generated id
            dataset = {
                "id": dataset_id,
                "name": name,
                "uploaded_by": uploaded_by,
                "data": data_json_str,
                "uploaded_at": response.data[0]["uploaded_at"]
            }
            self._datasets[dataset_id] = dataset
            return {"status": "success", "dataset_id": dataset_id, "uploaded_at": dataset["uploaded_at"]}
        else:
            return {"status": "error", "message": "Failed to insert into Supabase."}

    def get_all_datasets(self):
        """Fetch all datasets from Supabase."""
        response = supabase.table("datasets").select("*").execute()
        if response.data:
            return response.data
        return []

    def get_dataset(self, dataset_id):
        """Get a single dataset from local cache."""
        return self._datasets.get(dataset_id)

    def remove_dataset(self, dataset_id):
        """Remove dataset from Supabase and local cache."""
        response = supabase.table("datasets").delete().eq("id", dataset_id).execute()
        if response.data:
            self._datasets.pop(dataset_id, None)
            return {"status": "success", "dataset_id": dataset_id}
        return {"status": "error", "message": "Dataset not found"}

# ---------------- Insight Manager ----------------
class InsightManager:
    def __init__(self, dataset_manager):
        self.insights = []
        self.dataset_manager = dataset_manager

    def generate_generic_summary(self, df: pd.DataFrame):
        """Generate a textual summary of the dataset."""
        if df.empty:
            return "The dataset is empty."

        summary_lines = [
            f"Rows: {len(df)}, Columns: {len(df.columns)}.",
            "Columns: " + ", ".join(df.columns),
            "Column types and non-null counts:"
        ]

        for col in df.columns:
            dtype = df[col].dtype
            non_null = df[col].notnull().sum()
            summary_lines.append(f" - {col}: {dtype}, non-null: {non_null}")

        numeric_cols = df.select_dtypes(include='number').columns
        if not numeric_cols.empty:
            summary_lines.append("Basic statistics for numeric columns:")
            for col in numeric_cols:
                summary_lines.append(
                    f" - {col}: mean={df[col].mean():.2f}, min={df[col].min()}, max={df[col].max()}, std={df[col].std():.2f}"
                )

        return "\n".join(summary_lines)

    def generate_plots(self, df: pd.DataFrame, insight_id: int):
        """Generate histograms for numeric columns."""
        os.makedirs("insight_plots", exist_ok=True)
        plots = []

        numeric_cols = df.select_dtypes(include='number').columns
        for col in numeric_cols:
            fig = plt.figure(figsize=(5, 3))
            ax = fig.add_subplot(111)
            df[col].plot.hist(ax=ax, bins=10)
            ax.set_title(f"Distribution of {col}")
            ax.set_xlabel(col)
            plt.tight_layout()

            fname = f"insight_plots/insight_{insight_id}_{col}_hist.png"
            fig.savefig(fname)
            plt.close(fig)
            plots.append(fname)

        return plots

    def add_insight(self, dataset_id, summary=None):
        """Add an insight for a given dataset."""
        dataset = self.dataset_manager.get_dataset(dataset_id)
        if not dataset:
            return {"status": "error", "message": "Dataset not found"}

        df = pd.DataFrame(dataset["data"])

        if summary is None:
            summary = self.generate_generic_summary(df)

        insight_id = len(self.insights) + 1
        plots = self.generate_plots(df, insight_id)

        insight = {
            "id": insight_id,
            "dataset_id": dataset_id,
            "summary": summary,
            "plots": plots
        }

        self.insights.append(insight)
        return {
            "status": "success",
            "message": "Insight added",
            "id": insight_id,
            "summary": summary,
            "plots": plots
        }

    def get_insights(self, dataset_id):
        """Get all insights for a given dataset."""
        return [
            {
                "id": ins["id"],
                "summary": ins["summary"],
                "plots": ins["plots"]
            }
            for ins in self.insights
            if ins["dataset_id"] == dataset_id
        ]

# ---------------- Manager Instances ----------------
dataset_manager = DatasetManager()
insight_manager = InsightManager(dataset_manager)
