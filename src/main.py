from fastapi import FastAPI
from src.api.routes.health import router as health_router
from src.api.routes.users import router as users_router
from src.api.routes.policies import router as policy_router

app = FastAPI(title="ClaimIQ", version="1.0.0")

app.include_router(health_router)
app.include_router(users_router)
app.include_router(policy_router)


@app.get("/")
def root():
    return {"message": "ClaimIQ API"}
