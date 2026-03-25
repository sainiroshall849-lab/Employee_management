"""
Employee Management System API
A FastAPI-based employee management application with CRUD operations.
"""

import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db.database import Base, engine
from Routes.employee_routes import router as employee_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/app.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Create FastAPI app with metadata
app = FastAPI(
    title="Employee Management System",
    description="A comprehensive API for managing employee records",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include employee routes
app.include_router(employee_router, prefix="/api/v1")

@app.on_event("startup")
def startup_event():
    """Initialize database tables on startup."""
    try:
        logger.info("Initializing database...")
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Failed to create database tables: {str(e)}")
        raise

@app.on_event("shutdown")
def shutdown_event():
    """Cleanup on application shutdown."""
    logger.info("Shutting down Employee Management API")

@app.get("/", tags=["Health"])
def root():
    """Health check endpoint."""
    return {
        "message": "Employee Management API is running",
        "status": "healthy",
        "version": "1.0.0"
    }

@app.get("/health", tags=["Health"])
def health_check():
    """Detailed health check."""
    return {
        "status": "healthy",
        "service": "Employee Management API",
        "database": "Connected"
    }

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting server...")
    uvicorn.run(app, host="0.0.0.0", port=8000)