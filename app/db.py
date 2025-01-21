import os
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from datetime import datetime
from loguru import logger

# Load environment variables
load_dotenv()

# Load MongoDB credentials from environment variables
MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME")

# Ensure environment variables are set
if not MONGO_URI or not DATABASE_NAME:
    logger.error("MONGO_URI or DATABASE_NAME is not set in the environment variables.")
    raise ValueError("MONGO_URI or DATABASE_NAME is missing.")

# Function to establish MongoDB connection with error handling
def get_mongo_client():
    try:
        client = MongoClient(MONGO_URI)
        # Ping to check connection
        client.admin.command('ping')
        logger.info("Successfully connected to MongoDB.")
        return client
    except PyMongoError as e:
        logger.error(f"MongoDB connection error: {e}")
        raise

# Function to perform database operations
def perform_db_operations():
    client = None
    try:
        # Get client and access database
        client = get_mongo_client()
        database = client[DATABASE_NAME]
        collection = database["test_collection"]

        # Sample document to insert
        sample_document = {
            "name": "Test Item",
            "description": "This is a test document for the MongoDB collection.",
            "created_at": datetime.utcnow()
        }

        # Insert a document with error handling
        result = collection.insert_one(sample_document)
        logger.info(f"Document inserted with ID: {result.inserted_id}")

        # Query the inserted document
        queried_document = collection.find_one({"name": "Test Item"})
        if queried_document:
            logger.info(f"Queried document: {queried_document}")
        else:
            logger.warning("Document not found.")

    except PyMongoError as e:
        logger.error(f"An error occurred during database operations: {e}")
    finally:
        if client:
            client.close()
            logger.info("MongoDB connection closed.")


