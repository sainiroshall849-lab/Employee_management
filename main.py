from fastapi import FastAPI
from db.database import Base, engine
from Routes.employee_routes import router as employee_router

app = FastAPI()

# Include routes
app.include_router(employee_router)

@app.on_event("startup")
def startup_event():
    """Create tables on server startup"""
    Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "Employee Management API Running"}