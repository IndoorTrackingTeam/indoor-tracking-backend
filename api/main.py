from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from src.app.routes import equipment, user, router_training_data, router_data, hospital_settings
import uvicorn

api = FastAPI()

api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)

api.include_router(user.router, prefix="/user", tags=["user"])
api.include_router(equipment.router, prefix="/equipment", tags=["equipment"])
api.include_router(router_training_data.router, prefix="/router/training-data", tags=["router-training-data"])
api.include_router(router_data.router, prefix="/router/data", tags=["router-data"])
api.include_router(hospital_settings.router, prefix="/settings", tags=["settings"])

if __name__ == "__main__":
    uvicorn.run("main:api", host="0.0.0.0", port=8000, reload=True)
    # uvicorn.run("main:api", host="0.0.0.0", port=8000, workers=2)
