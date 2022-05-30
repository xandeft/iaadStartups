from fastapi import APIRouter, Depends, status, HTTPException, Request, Response, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import schemas, models, database

router = APIRouter(
    prefix = "/startup",
    tags = ['Startups']
)

get_db = database.get_db

templates = Jinja2Templates(directory="templates")

def getDeveloperName(id, db: Session = Depends(get_db)):
    developer = db.query(models.Programador).filter(models.Programador.id_programador == id).first()

    if not developer:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f'The developer with the id {id} is not found')

    return developer.__dict__['nome_programador']

def getDevsOfStartup(id_startup, db: Session = Depends(get_db)):
    developer = db.query(models.Programador).filter(models.Programador.id_startup == id_startup)

    devs = []

    if not developer.first():
        return []
        #raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f'The developer with the id {id} is not found')

    for i in developer.all():

        devs.append(getDeveloperName(i.__dict__['id_programador'], db))

    return devs


@router.get("/createui", response_class=HTMLResponse)
def create_startup_ui(request: Request):
    return templates.TemplateResponse("/startup_pages/new_startup.html", {"request": request})

@router.post('', status_code=status.HTTP_201_CREATED, response_class = HTMLResponse)
def createStartup(request: Request, db: Session = Depends(get_db), nome_startup: str = Form(...), cidade_sede: str = Form(...)):
    new_startup = models.Startup(nome_startup=nome_startup, cidade_sede=cidade_sede)

    db.add(new_startup)

    db.commit()

    db.refresh(new_startup)

    return getAllStartups(request, db)

@router.get('', response_class = HTMLResponse)
def getAllStartups(request: Request, db: Session = Depends(get_db)):
    startups = db.query(models.Startup).all()
    return templates.TemplateResponse('/startup_pages/list_startups.html', {'request': request, 'startup_list': startups})


@router.get('/{id}', response_model = schemas.showStartup, response_class = HTMLResponse)
def getStartup(id, request: Request, db: Session = Depends(get_db)):
    startup = db.query(models.Startup).filter(models.Startup.id_startup == id).first()

    if not startup:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f'The startup with the id {id} is not found')

    startup = startup.__dict__
    devs = getDevsOfStartup(startup['id_startup'], db)
    startup["devs"] = devs
    startup["lenDevs"] = len(devs)
    return templates.TemplateResponse("/startup_pages/view_startup.html", {"request": request, "startup": startup})


@router.get("/edit/{id}", response_class=HTMLResponse)
def edit_startup(id:int, response:Response, request:Request, db: Session = Depends(get_db)):
    startup = db.query(models.Startup).filter(models.Startup.id_startup == id).first()
    return templates.TemplateResponse("/startup_pages/edit_startup.html", {"request": request, "startup": startup})

@router.post('/update/{id}', status_code = status.HTTP_202_ACCEPTED, response_class = HTMLResponse)
def updateStartup(id, request: Request, response: Response, db: Session = Depends(get_db), id_startup:int = Form(...), nome_startup:str = Form(...), cidade_sede:str = Form(...)):
    startup = db.query(models.Startup).filter(models.Startup.id_startup == id)

    if not startup.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f'The startup with the id {id} is not found')

    updatedStartup = {
        'id_startup': id_startup,
        'nome_startup': nome_startup,
        'cidade_sede': cidade_sede
    }

    startup.update(updatedStartup)
    db.commit()

    return getAllStartups(request, db)

@router.get('/delete/{id}', status_code = status.HTTP_204_NO_CONTENT, response_class = HTMLResponse)
def deleteStartup(id:int, request: Request, db: Session = Depends(get_db)):
    startup = db.query(models.Startup).filter(models.Startup.id_startup == id)

    if not startup.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f'The startup with the id {id} is not found')

    startup.delete(synchronize_session=False)
    db.commit()
    return getAllStartups(request, db)