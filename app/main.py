from fastapi import FastAPI, HTTPException
from loguru import logger
import uvicorn

from contextlib import asynccontextmanager
from db import perform_db_operations


# Define lifespan event handler
@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        # Perform initial database operations when the app starts
        logger.info("Performing initial database operations...")
        perform_db_operations()
        yield
    except Exception as e:
        logger.critical(f"Unexpected error during startup: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Database connection failed during startup")
    finally:
        logger.info("Closing application")


# Create FastAPI app with the lifespan handler
app = FastAPI(title="E-Commerce API", lifespan=lifespan)


# Example route
@app.get("/")
async def read_root():
    return {"message": "Welcome to the E-Commerce API!"}


# Entry point to run the app using uvicorn
if __name__ == "__main__":
    try:
        logger.info("Starting FastAPI")
        uvicorn.run(app, host="0.0.0.0", port=8000)
    except Exception as e:
        logger.critical(f"Unexpected error while starting FastAPI: {e}", exc_info=True)
