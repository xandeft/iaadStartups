import models, database
from fastapi import FastAPI, Request, Response, status
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import uvicorn
from routers import startup, language, developer, devlanguages



app = FastAPI()

models.Base.metadata.create_all(database.engine)

app.mount('/static', StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get('/', response_class=HTMLResponse)
def home_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

app.include_router(startup.router)
app.include_router(developer.router)
app.include_router(language.router)
app.include_router(devlanguages.router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port = '8000')



