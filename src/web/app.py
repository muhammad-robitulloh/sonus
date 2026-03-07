import os
import sys
from fastapi import FastAPI, UploadFile, File, Form, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import shutil

# Add project src to path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__))))
from core.brain import SonusBrain

app = FastAPI(title="Sonus AI Co-Producer Dashboard")
brain = SonusBrain()

# Directory for uploads
UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data")
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

# Templates setup
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "templates"))

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """The main dashboard view (Web Dashboard)."""
    return templates.TemplateResponse("index.html", {"request": request, "standards": brain.knowledge['standards']})

@app.post("/upload")
async def upload_audio(file: UploadFile = File(...)):
    """Upload audio file for analysis."""
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    brain.load_track(file_path)
    return {"filename": file.filename, "status": "loaded"}

@app.get("/critique")
async def get_critique(label: str = None):
    """Perform deep analysis for the current loaded track."""
    report = brain.critique_production(label_key=label)
    return JSONResponse(content=report)

@app.get("/vibe")
async def get_vibe():
    """Extract mood, energy, and rhythm features."""
    report = brain.deep_vibe_analysis()
    return JSONResponse(content=report)

@app.get("/recipes")
async def get_vst_recipe(plugin: str = "serum", patch: str = "ophelia_bass"):
    """Fetch VST parameter recipes."""
    recipe = brain.get_vst_recipe(plugin, patch)
    return {"plugin": plugin, "patch": patch, "data": recipe}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
