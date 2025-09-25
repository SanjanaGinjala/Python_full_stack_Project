import pandas as pd
from src.db import DatabaseManager

class DatasetManager:
    """Handles all dataset-related operations"""
    def __init__(self):
        self.db = DatabaseManager()

    def add_dataset(self, name, uploaded_by, csv_file_path):
        try:
            df = pd.read_csv(csv_file_path)
            data_json = df.to_dict(orient="records")
            response = self.db.save_dataset(name, uploaded_by, data_json)
            if response:
                return {"status": "success", "message": "Dataset added successfully!"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def get_all_datasets(self):
        return self.db.get_all_datasets()

    def get_dataset(self, dataset_id):
        return self.db.get_dataset_by_id(dataset_id)

    def remove_dataset(self, dataset_id):
        response = self.db.delete_dataset(dataset_id)
        if response:
            return {"status": "success", "message": "Dataset deleted successfully!"}
        return {"status": "error", "message": "Failed to delete dataset"}


class InsightManager:
    """Handles all insight-related operations"""
    def __init__(self):
        self.db = DatabaseManager()

    def add_insight(self, dataset_id, summary, charts=None):
        response = self.db.save_insight(dataset_id, summary, charts)
        if response:
            return {"status": "success", "message": "Insight added successfully!"}
        return {"status": "error", "message": "Failed to add insight"}

    def get_insights(self, dataset_id):
        return self.db.get_insights_by_dataset(dataset_id)

    def remove_insight(self, insight_id):
        response = self.db.delete_insight(insight_id)
        if response:
            return {"status": "success", "message": "Insight deleted successfully!"}
        return {"status": "error", "message": "Failed to delete insight"}
