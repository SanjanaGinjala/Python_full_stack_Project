# TrendTeller-DataMadeSimple

A Python-powered tool that turns raw datasets into easy-to-understand charts and summaries. Upload your CSV, and TrendTeller automatically generates visualizations and key insights, helping you understand trends and anomalies in your data — all stored and managed with Supabase.

## Features
-- Upload CSV – Users can upload any dataset.

--Automatic Analysis – Calculates totals, averages, trends.

--Charts & Graphs – Creates visual graphs like bar, line, and pie charts.

--Easy-to-Read Insights – Converts data into simple plain-language summaries.

--Anomaly Detection – Highlights unusual data points automatically.

--Save Data & Insights – All datasets, charts, and summaries stored in Supabase.

## Project Structure

TRENDTELLER/
|
|---src/            # core application logic
|   |---logic.py    # Buisiness logic and task
operations
|   |__db.py        # Database operations
|
|----api/           # Backend API
|   |__main.py      # FastAPI
|
|----frontend/      # Frontend application
|     |__app.py     # Streamlit web interface
|
|____requirements.txt  # Python Dependencies
|
|____Readme.md      # Project documentation
|
|____.env           # python Variables

## Quck Start

### Prerequisites

- Python 3.8 or higher
- A Supabase account
- Git(Push,cloning)

### 1.Clone or Download the Project
# Option 1.Clone with Git
git clone <repository-url>

# Option 2:Download and extract the ZIP file

### 2.Install Dependencies

# Install all required python packages
pip install -r requirements.txt

### 3.Set Up a Supabase Database

1.Create a Supabase Project:

2.Create the Tasks Table:
- Go to the SQL Editor in your Supabase dashboard
-Run this SQL Command:

'''
    CREATE TABLE datasets (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    uploaded_by TEXT,
    data JSON NOT NULL,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

'''