# backend/app/api/recommend.py
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from fastapi import APIRouter  # type: ignore
else:
    try:
        from fastapi import APIRouter
    except Exception:
        # Minimal fallback so the module can be imported/tested without FastAPI installed.
        class APIRouter:
            def post(self, *args, **kwargs):
                def decorator(func):
                    return func
                return decorator
from pydantic import BaseModel
from app.utils.embedding_utils import embed_text
from app.utils.pinecone_utils import query_index
from app.utils.generator import generate_blurb

router = APIRouter()

class QueryRequest(BaseModel):
    prompt: str
    k: int = 5

@router.post("/query")
async def get_recommendations(req: QueryRequest):
    vec = embed_text(req.prompt)
    results = query_index(vec.tolist(), top_k=req.k)

    # enrich results with generated text
    enriched = []
    for r in results:
        meta = r["metadata"]
        blurb = generate_blurb(meta)
        enriched.append({
            "uniq_id": meta["uniq_id"],
            "title": meta["title"],
            "brand": meta["brand"],
            "price": meta["price"],
            "categories": meta["categories"],
            "color": meta["color"],
            "material": meta["material"],
            "score": r["score"],
            "gen_description": blurb
        })
    return {"results": enriched}

from app.models.image_classifier import predict_image_category

# within loop:
pred_label = None
if meta.get("images"):
    first_img = meta["images"].split(",")[0].strip("[]'\" ")
    pred_label = predict_image_category(first_img)
meta["predicted_label"] = pred_label
