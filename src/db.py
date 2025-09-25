import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

supabase = create_client(url, key)


# Dataset functions
def save_dataset(name, uploaded_by, data):
    response = supabase.table("datasets").insert({
        "name": name,
        "uploaded_by": uploaded_by,
        "data": data
    }).execute()
    return response

def get_all_datasets():
    response = supabase.table("datasets").select("*").execute()
    return response.data

def get_dataset_by_id(dataset_id):
    response = supabase.table("datasets").select("*").eq("id", dataset_id).execute()
    return response.data[0] if response.data else None

def delete_dataset(dataset_id):
    response = supabase.table("datasets").delete().eq("id", dataset_id).execute()
    return response


# Insights functions
def save_insight(dataset_id, summary, charts=None):
    response = supabase.table("insights").insert({
        "dataset_id": dataset_id,
        "summary": summary,
        "charts": charts
    }).execute()
    return response

def get_insights_by_dataset(dataset_id):
    response = supabase.table("insights").select("*").eq("dataset_id", dataset_id).execute()
    return response.data

def delete_insight(insight_id):
    response = supabase.table("insights").delete().eq("id", insight_id).execute()
    return response


# Users functions
def create_user(username, email):
    response = supabase.table("users").insert({
        "username": username,
        "email": email
    }).execute()
    return response

def get_all_users():
    response = supabase.table("users").select("*").execute()
    return response.data

def get_user_by_id(user_id):
    response = supabase.table("users").select("*").eq("id", user_id).execute()
    return response.data[0] if response.data else None

def delete_user(user_id):
    response = supabase.table("users").delete().eq("id", user_id).execute()
    return response
