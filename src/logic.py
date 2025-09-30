import pandas as pd
import matplotlib.pyplot as plt
import os

# ---------------- Dataset Manager ----------------
from datetime import datetime

class DatasetManager:
    def __init__(self):
        self._datasets = {}
        self._next_id = 1

    def add_dataset(self, name, uploaded_by, data_json):
        dataset_id = self._next_id
        self._next_id += 1

        self._datasets[dataset_id] = {
            "id": dataset_id,
            "name": name,
            "uploaded_by": uploaded_by,
            "data": data_json,
            "uploaded_at": datetime.utcnow().isoformat()
        }

        return {
            "status": "success",
            "dataset_id": dataset_id,
            "uploaded_at": self._datasets[dataset_id]["uploaded_at"]
        }

    def get_all_datasets(self):
        return list(self._datasets.values())

    def get_dataset(self, dataset_id):
        return self._datasets.get(dataset_id)

    def remove_dataset(self, dataset_id):
        if dataset_id in self._datasets:
            del self._datasets[dataset_id]
            return {"status": "success", "dataset_id": dataset_id}
        return {"status": "error", "message": "Dataset not found"}


# ---------------- Insight Manager ----------------
import pandas as pd
import matplotlib.pyplot as plt
import os

class InsightManager:
    def __init__(self, dataset_manager):
        self.insights = []
        self.dataset_manager = dataset_manager

    def generate_generic_summary(self, df: pd.DataFrame):
        if df.empty:
            return "The dataset is empty."

        summary_lines = []

        # Basic structure
        summary_lines.append(f"Rows: {len(df)}, Columns: {len(df.columns)}.")

        # Column names
        summary_lines.append("Columns: " + ", ".join(df.columns))

        # Column types and non-null counts
        summary_lines.append("Column types and non-null counts:")
        for col in df.columns:
            dtype = df[col].dtype
            non_null = df[col].notnull().sum()
            summary_lines.append(f" - {col}: {dtype}, non-null: {non_null}")

        # Simple stats for numeric columns
        numeric_cols = df.select_dtypes(include='number').columns
        if not numeric_cols.empty:
            summary_lines.append("Basic statistics for numeric columns:")
            for col in numeric_cols:
                summary_lines.append(
                    f" - {col}: mean={df[col].mean():.2f}, min={df[col].min()}, max={df[col].max()}, std={df[col].std():.2f}"
                )

        return "\n".join(summary_lines)

    def generate_plots(self, df: pd.DataFrame, insight_id: int):
        os.makedirs("insight_plots", exist_ok=True)
        plots = []

        # Plot histograms for numeric columns
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
        dataset = self.dataset_manager.get_dataset(dataset_id)
        if not dataset:
            return {"status": "error", "message": "Dataset not found"}

        df = pd.DataFrame(dataset["data"])

        # Auto-generate summary if not provided
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
