from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Any
import pandas as pd
import io, sys, os

# Add src.logic to sys.path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from src.logic import dataset_manager, InsightManager

# Initialize Insight Manager
insight_manager = InsightManager(dataset_manager)

# Create FastAPI app
app = FastAPI(title="TrendTeller", version="1.0")

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- Pydantic Models ----------

class InsightRequest(BaseModel):
    dataset_id: int
    summary: Optional[str] = None

class DatasetResponse(BaseModel):
    status: str
    dataset_id: Optional[int] = None
    message: Optional[str] = None
    uploaded_at: Optional[str] = None

class DatasetDetail(BaseModel):
    id: int
    name: str
    uploaded_by: str
    data: List[Any]
    uploaded_at: str

# ---------- Root ----------

@app.get("/")
def root():
    return {"message": "🚀 TrendTeller API is running!"}

# ---------- Upload Dataset ----------

@app.post("/datasets/", response_model=DatasetResponse)
def add_dataset(
    name: str = Form(...),
    uploaded_by: str = Form(...),
    file: UploadFile = File(...)
):
    try:
        contents = file.file.read()
        df = pd.read_csv(io.BytesIO(contents))

        # Accept any columns
        data_json = df.to_dict(orient="records")

        # Add dataset to manager
        result = dataset_manager.add_dataset(name, uploaded_by, data_json)

        if result.get("status") == "error":
            raise HTTPException(status_code=400, detail=result.get("message"))

        return result

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Upload failed: {str(e)}")

# ---------- Get All Datasets ----------

@app.get("/datasets/", response_model=List[DatasetDetail])
def get_all_datasets():
    datasets = dataset_manager.get_all_datasets()

    valid_datasets = []
    for ds in datasets:
        if {"id", "name", "uploaded_by", "data", "uploaded_at"}.issubset(ds.keys()):
            valid_datasets.append(ds)
        else:
            print(f"⚠️ Skipping invalid dataset: {ds}")
    return valid_datasets

# ---------- Get Single Dataset ----------

@app.get("/datasets/{dataset_id}", response_model=DatasetDetail)
def get_dataset(dataset_id: int):
    ds = dataset_manager.get_dataset(dataset_id)
    if not ds:
        raise HTTPException(status_code=404, detail="Dataset not found")
    return ds

# ---------- Delete Dataset ----------

@app.delete("/datasets/{dataset_id}", response_model=DatasetResponse)
def delete_dataset(dataset_id: int):
    result = dataset_manager.remove_dataset(dataset_id)
    if result.get("status") == "error":
        raise HTTPException(status_code=400, detail=result.get("message"))
    return result

# ---------- Insights ----------

@app.post("/insights/")
def add_insight(insight: InsightRequest):
    result = insight_manager.add_insight(insight.dataset_id, insight.summary)
    if result.get("status") == "error":
        raise HTTPException(status_code=400, detail=result.get("message"))
    return result

@app.get("/insights/{dataset_id}")
def get_insights(dataset_id: int):
    return insight_manager.get_insights(dataset_id)
