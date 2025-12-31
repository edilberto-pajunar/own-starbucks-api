from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routers.v1 import drinks, custom_drinks, favorites


app = FastAPI(
    title="Own Starbucks", version="0.1.0",
)

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")


@app.get("/")
def root():
    return {"message": "Hello World!"}

app.include_router(drinks.router, tags=["drinks"])
app.include_router(custom_drinks.router, tags=["custom_drinks"])
app.include_router(favorites.router, tags=["favorites"])


