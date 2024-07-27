from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import books, reviews,user_routes,summary
from sql_app.database import engine, Base
from load_model_data import load_model

app = FastAPI()

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust as necessary
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        # Create tables
        await conn.run_sync(Base.metadata.create_all)

# Load the model and data on startup
@app.on_event("startup")
async def load_model_and_data():
    global model, df,label_encoder
    
    model,df,label_encoder=load_model()

app.include_router(books.router)
app.include_router(reviews.router)
app.include_router(summary.router)
app.include_router(user_routes.router)
