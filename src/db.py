# Simple in-memory DB for testing

class DatabaseManager:
    def __init__(self):
        self.datasets = {}
        self.insights = {}
        self.dataset_counter = 1
        self.insight_counter = 1

    # Dataset methods
    def save_dataset(self, name, uploaded_by, data):
        dataset_id = self.dataset_counter
        self.datasets[dataset_id] = {
            "id": dataset_id,
            "name": name,
            "uploaded_by": uploaded_by,
            "data": data
        }
        self.dataset_counter += 1
        return True

    def get_all_datasets(self):
        return list(self.datasets.values())

    def get_dataset_by_id(self, dataset_id):
        return self.datasets.get(dataset_id)

    def delete_dataset(self, dataset_id):
        if dataset_id in self.datasets:
            del self.datasets[dataset_id]
            return True
        return False

    # Insight methods
    def save_insight(self, dataset_id, summary, charts=None):
        if dataset_id not in self.datasets:
            return False
        insight_id = self.insight_counter
        self.insights[insight_id] = {
            "id": insight_id,
            "dataset_id": dataset_id,
            "summary": summary,
            "charts": charts or {}
        }
        self.insight_counter += 1
        return True

    def get_insights_by_dataset(self, dataset_id):
        return [insight for insight in self.insights.values() if insight["dataset_id"] == dataset_id]

    def delete_insight(self, insight_id):
        if insight_id in self.insights:
            del self.insights[insight_id]
            return True
        return False
