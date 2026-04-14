from fastapi import FastAPI
from routers import ahp_router
from routers import rental_router
from routers import auth_router
from routers import admin_router
from fastapi.staticfiles import StaticFiles
from routers import upload_router
from routers import import_router
app = FastAPI()

app.include_router(ahp_router.router)
app.include_router(rental_router.router)
app.include_router(auth_router.router)
app.include_router(admin_router.router)
app.include_router(upload_router.router)
app.include_router(import_router.router)

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
@app.get("/")
def root():
    return {"message": "DSS Rental System API"}