from fastapi import FastAPI, Request, Depends, Form, HTTPException, status, File, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from datetime import datetime

# Local Imports
from modules.Spotify_.SpotifyAPI import SpotifyAPIUtility
from modules.json_helper.json_helper import dump_file, read_file
from modules.playlist.PlaylistUtility import make_recommendation_playlist,embedd_playlist

app = FastAPI()

# Mount static files and configure templates
templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

# Mount the 'data' directory at the '/data' path
app.mount("/data", StaticFiles(directory="data"), name="data")


@app.get("/index", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/discover-music", response_class=HTMLResponse)
async def discover_music(request: Request, recommendation_params: dict):
    playlist = make_recommendation_playlist(recommendation_params)
    
    if 'error' in playlist:
        return HTMLResponse(content=playlist['error'], media_type='text/html')
    else:
        embedd_html = embedd_playlist(playlist['playlist_id'])
        print(embedd_html)
        return HTMLResponse(content=embedd_html, media_type='text/html')
    
@app.get("/test", response_class=HTMLResponse)
async def test(request: Request):
    return templates.TemplateResponse("test.html", {"request": request})    
    