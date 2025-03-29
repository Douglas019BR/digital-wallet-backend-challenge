from fastapi import FastAPI

from config.database import Base, engine
from controllers.user_controller import user_router

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(user_router, prefix="/users", tags=["users"])


@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI MVC Boilerplate!"}
