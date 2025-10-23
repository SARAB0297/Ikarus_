# backend/app/api/analytics.py
from fastapi import APIRouter
import pandas as pd
import os

router = APIRouter()
DATA_PATH = os.path.join("data", "preprocessed_products.csv")

@router.get("/analytics/summary")
async def get_summary():
    df = pd.read_csv(DATA_PATH)
    summary = {
        "num_products": len(df),
        "avg_price": round(df["price"].mean(), 2),
        "max_price": float(df["price"].max()),
        "min_price": float(df["price"].min()),
        "top_categories": df["primary_category"].value_counts().head(5).to_dict()
    }
    return summary
