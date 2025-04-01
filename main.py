from fastapi import FastAPI

from controllers.auth_controller import login_router
from controllers.user_controller import user_router
from controllers.wallet_controller import router as wallet_router

app = FastAPI()


app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(login_router, prefix="/login", tags=["login"])
app.include_router(wallet_router, prefix="/wallets", tags=["wallets"])


@app.get("/health")
def health_check():
    return {"status": "ok"}
