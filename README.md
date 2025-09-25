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
|   |---logic.py    # Business logic and task
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

## Quick Start

### Prerequisites

- Python 3.8 or higher
- A Supabase account
- Git(Push,cloning)

### 1.Clone or Download the Project
# Option 1.Clone with Git
git clone <repository-url>

# Option 2:Download and extract the ZIP file

### 2.Install Dependencies

# Install Dependencies
pip install -r requirements.txt

### 3.Set Up a Supabase Database

1.Create a Supabase Project:

2.Create the datasets table in SQL Editor:
- Go to the SQL Editor in your Supabase dashboard
-Run this SQL Command:

```
    CREATE TABLE datasets (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    uploaded_by TEXT,
    data JSON NOT NULL,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

3. **Get Your Credentials:

### 4.Configure Environment Variables

1.create a `.env` file in the project root

2.Add your Supabase credentials to `.env`:
SUPABASE_URL="https:/...."
SUPABASE_KEY="..."
### 5.Run the Application

## Streamlit Frontend
streamlit run frontend/app.py

The app will open in your browser at `http://localhost:8501`

## FastAPI Backend

cd api
python main.py

The API will be available at `http://localhost:8000`

## How to Use
---Upload a CSV file through the Streamlit interface.

---View the dataset preview, charts, and generated summaries.

---Save the dataset and insights to Supabase for later access.

## Technical Details:

### Technologies used

**Frontend**:Streamlit (Python web frameworj)
**Backend**: fastAPI (Python REST API framework)
**Database**:Supabase(PostgreSQL-based backend-as-a-service)
**Language**:Python 3.8+


### Key Components

1.**`src/db.py`**: Database operations 
-Handles all CRUD operations with Supabase

2.**`src/logic.py`** : Buisiness logic 
-Task validation and processing

## Troubleshooting

## Common Issues

1.**"Module not Found" errors**
    -Make sure you've installed all dependencies:`pip install -r requirements.txt`

## Future Enhancements

Ideas for Extending this projects:

---Interactive dashboard for multiple datasets

---AI-powered natural language summaries

---Multi-user support

---Export insights and charts as PDF or Excel

---Advanced anomaly detection

## Support

If you encounter any issues or have questions:..
