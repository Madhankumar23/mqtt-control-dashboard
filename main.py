from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import json

app = FastAPI()

# Set up Jinja2 templates and static files
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Load user data from file
import os

file_path = os.path.join(os.path.dirname(__file__), "users.json")
with open(file_path) as f:
    users = json.load(f)


@app.get("/", response_class=HTMLResponse)
def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "error": ""})

@app.post("/login", response_class=HTMLResponse)
def login(request: Request, username: str = Form(...), password: str = Form(...)):
    if username in users and users[username] == password:
        return RedirectResponse(url="/dashboard", status_code=302)
    else:
        return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid username or password"})

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})
