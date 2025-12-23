from fastapi import FastAPI
from app.routers.v1 import customized_drinks
from app.routers.v1 import drinks


app = FastAPI(
    title="Own Starbucks", version="0.1.0",
)


@app.get("/")
def root():
    return {"message": "Hello World!"}

app.include_router(drinks.router, tags=["drinks"])
app.include_router(customized_drinks.router, tags=["customized_drinks"])


