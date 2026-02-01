from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.database.database import connect_to_mongo, close_mongo_connection
from commons.loggers import logger

logging = logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    logging.info("Starting up Hotel Management System API...")
    await connect_to_mongo()
    yield
    # Shutdown logic
    logging.info("Shutting down Hotel Management System API...")
    await close_mongo_connection()


app = FastAPI(
    title="Hotel Management System API",
    description="Enterprise-grade platform for managing hotel operations and guest bookings.",
    version="1.0.0",
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Check Hotels"])
async def Check_Hotels():
    """
    Check if the API is running.
    """
    return {
        "status": "Checked",
        "service": "Hotel Management System API",
        "version": "1.0.0",
    }


@app.get("/", include_in_schema=False)
async def root():
    return {"message": "Welcome to the Hotel Management System API"}
