from fastapi import FastAPI

from controllers.auth_controller import login_router
from controllers.user_controller import user_router

app = FastAPI()


# Base.metadata.create_all(bind=engine)
# Uncomment this line to create all tables in the database

app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(login_router, prefix="/login", tags=["login"])


@app.get("/health")
def health_check():
    return {"status": "ok"}
