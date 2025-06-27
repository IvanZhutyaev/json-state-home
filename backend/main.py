from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from Routers import Zastroy_router, User_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # или "*" для разработки
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(Zastroy_router.router)
app.include_router(User_router.router)


@app.get("/items/")
async def read_items():
    return [{"name": "Item 1"}]





