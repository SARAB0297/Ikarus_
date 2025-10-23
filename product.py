# backend/app/api/product.py
from fastapi import APIRouter, HTTPException
import pandas as pd
import os

router = APIRouter()
DATA_PATH = os.path.join("data", "preprocessed_products.csv")
df = pd.read_csv(DATA_PATH)

@router.get("/product/{uniq_id}")
async def get_product(uniq_id: str):
    item = df[df["uniq_id"] == uniq_id]
    if item.empty:
        raise HTTPException(status_code=404, detail="Product not found")
    return item.to_dict(orient="records")[0]
