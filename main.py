import os
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from database import create_document, get_documents, db
from schemas import TattooProduct, Review, GalleryItem, ContactMessage

app = FastAPI(title="Barcelona Tattoo Studio API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Health & Diagnostics
# -----------------------------

@app.get("/")
def read_root():
    return {"message": "Barcelona Tattoo Studio API is running"}

@app.get("/api/hello")
def hello():
    return {"message": "Hola from Barcelona!"}

@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }

    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = getattr(db, 'name', None) or ("✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set")
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:80]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:120]}"

    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"

    return response

# -----------------------------
# API: Products, Reviews, Gallery, Contact
# -----------------------------

class ListResponse(BaseModel):
    items: list

# Sample fallback data (used only if DB is unavailable)
SAMPLE_PRODUCTS = [
    {
        "title": "Barcelona Blackwork Print",
        "description": "Limited A3 print inspired by Gothic Quarter motifs.",
        "price": 45.0,
        "image_url": "https://images.unsplash.com/photo-1543163521-1bf539c55dd2?q=80&w=1600&auto=format&fit=crop",
        "category": "prints",
        "in_stock": True,
    },
    {
        "title": "Flash Voucher",
        "description": "Gift a flash piece – redeemable in studio.",
        "price": 120.0,
        "image_url": "https://images.unsplash.com/photo-1543362906-acfc16c67564?q=80&w=1600&auto=format&fit=crop",
        "category": "voucher",
        "in_stock": True,
    },
]

SAMPLE_REVIEWS = [
    {
        "name": "Lucía",
        "rating": 5,
        "comment": "Clean lines, chill vibes. My favorite piece so far!",
        "avatar_url": "https://images.unsplash.com/photo-1502685104226-ee32379fefbe?w=200&h=200&fit=crop&crop=faces",
    },
    {
        "name": "Marc",
        "rating": 5,
        "comment": "Professional and creative. Loved the custom stencil.",
        "avatar_url": "https://images.unsplash.com/photo-1527980965255-d3b416303d12?w=200&h=200&fit=crop&crop=faces",
    },
]

SAMPLE_GALLERY = [
    {
        "image_url": "https://images.unsplash.com/photo-1520975916090-3105956dac38?q=80&w=1600&auto=format&fit=crop",
        "title": "Neo-trad Panther",
        "tags": ["neo-trad", "color"],
    },
    {
        "image_url": "https://images.unsplash.com/photo-1520975940507-39a4d0ec1c40?q=80&w=1600&auto=format&fit=crop",
        "title": "Blackwork Serpent",
        "tags": ["blackwork", "linework"],
    },
    {
        "image_url": "https://images.unsplash.com/photo-1514311548101-**?q=80&w=1600&auto=format&fit=crop",
        "title": "Barcelona Tile",
        "tags": ["pattern", "ornamental"],
    },
]

@app.get("/api/products", response_model=ListResponse)
def list_products():
    try:
        items = get_documents("tattooproduct", {}, limit=50)
        return {"items": items}
    except Exception:
        # Fallback to sample data for demo
        return {"items": SAMPLE_PRODUCTS}

@app.get("/api/reviews", response_model=ListResponse)
def list_reviews():
    try:
        items = get_documents("review", {}, limit=50)
        return {"items": items}
    except Exception:
        return {"items": SAMPLE_REVIEWS}

@app.get("/api/gallery", response_model=ListResponse)
def list_gallery():
    try:
        items = get_documents("galleryitem", {}, limit=60)
        return {"items": items}
    except Exception:
        return {"items": SAMPLE_GALLERY}

@app.post("/api/contact")
def submit_contact(message: ContactMessage):
    try:
        _id = create_document("contactmessage", message)
        return {"ok": True, "id": _id}
    except Exception:
        # Accept the message in demo mode even without DB
        return {"ok": True, "id": None}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
