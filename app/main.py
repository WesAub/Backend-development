# app/main.py

from fastapi import FastAPI
import uvicorn
from app.db import database, User


app = FastAPI()


@app.post("/user/", response_model=User)
def create_user(user:User):
    return user



@app.get("/")
async def read_root():
    return await User.objects.all()


@app.on_event("startup")
async def startup():
    if not database.is_connected:
        await database.connect()
    # create a dummy entry
    await User.objects.get_or_create(email="test@test.com")


@app.on_event("shutdown")
async def shutdown():
    if database.is_connected:
        await database.disconnect()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)