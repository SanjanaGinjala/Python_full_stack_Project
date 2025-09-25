#Frontend-->API-->logic-->db-->Response

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sys,os

# Add src folder to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from src.logic import DatasetManager, InsightManager

# ------------ App Setup ---------------
app = FastAPI(title="TrendTeller", version="1.0")

# Allow frontend (Streamlit) to call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # corrected
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------- Create Manager Instances -----------
dataset_manager = DatasetManager()
insight_manager = InsightManager()

# --------------- Pydantic Models ---------------
class DatasetModel(BaseModel):
    name: str
    uploaded_by: str
    csv_file_path: str

class InsightModel(BaseModel):
    dataset_id: int
    summary: str
    charts: dict | None = None

# --------------- API Endpoints ----------------

@app.post("/datasets/")
def add_dataset(dataset: DatasetModel):
    result = dataset_manager.add_dataset(dataset.name, dataset.uploaded_by, dataset.csv_file_path)
    if result["status"] == "error":
        raise HTTPException(status_code=400, detail=result["message"])
    return result

@app.get("/datasets/")
def get_all_datasets():
    return dataset_manager.get_all_datasets()

@app.get("/datasets/{dataset_id}")
def get_dataset(dataset_id: int):
    dataset = dataset_manager.get_dataset(dataset_id)
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    return dataset

@app.delete("/datasets/{dataset_id}")
def delete_dataset(dataset_id: int):
    result = dataset_manager.remove_dataset(dataset_id)
    if result["status"] == "error":
        raise HTTPException(status_code=400, detail=result["message"])
    return result

@app.post("/insights/")
def add_insight(insight: InsightModel):
    result = insight_manager.add_insight(insight.dataset_id, insight.summary, insight.charts)
    if result["status"] == "error":
        raise HTTPException(status_code=400, detail=result["message"])
    return result

@app.get("/insights/{dataset_id}")
def get_insights(dataset_id: int):
    return insight_manager.get_insights(dataset_id)
