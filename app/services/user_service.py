from hashlib import sha256

from db import get_mongo_client
from schemas.user_schema import UserCreateSchema


# Hash the password before storing it
def hash_password(password: str) -> str:
    return sha256(password.encode()).hexdigest()


# Create user in MongoDB
async def create_user(user: UserCreateSchema, db: get_mongo_client):
    collection = db.get_mongo_client("users")
    user_data = user.dict()
    user_data['password'] = hash_password(user_data['password'])
    result = collection.insert_one(user_data)
    return str(result.inserted_id)


# Get user by email (check if email already exists)
async def get_user_by_email(email: str):
    collection = get_mongo_client("users")
    return await collection.find_one({"email": email})
