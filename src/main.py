from fastapi import FastAPI
from src.auth.models import Base
from src.auth.router import router as auth_router
from src.tasks.router import router as task_router
from src.files.router import router as file_router


app = FastAPI(tiltle="Taskflow API")

# include the router
app.include_router(auth_router)
app.include_router(task_router)
app.include_router(file_router)

@app.get("/")
def root():
    return {"message": "The server is working!"}