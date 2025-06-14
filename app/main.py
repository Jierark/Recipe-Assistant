from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from dotenv import load_dotenv


load_dotenv()

app = FastAPI(
    title="Recipe Assistant API",
    description="A smart recipe management assistant",
    version="1.0.0"
)
#CORS = Cross Origin Resource Sharing, lets web apps interact with other web apps
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], #change this 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory='static'), name="static")

#Imports all the routes
from app.routes import recipe_routes

app.include_router(recipe_routes.router, prefix="/api")

@app.get("/health")
async def health_check():
    return {'status': 'healthy'}

@app.get("/")
async def root():
    return FileResponse("index.html")
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8000)