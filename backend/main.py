from fastapi import FastAPI
from routers import ahp_router
from routers import rental_router

app = FastAPI()

app.include_router(ahp_router.router)
app.include_router(rental_router.router)

@app.get("/")
def root():
    return {"message": "DSS Rental System API"}