from typing import List
from fastapi import APIRouter, Depends, status, HTTPException, Request, Response, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import schemas, models, database

router = APIRouter(
    prefix = "/programador",
    tags = ['Developers']
)

get_db = database.get_db

templates = Jinja2Templates(directory="templates")


@router.get("/createui", response_class=HTMLResponse)
def create_startup_ui(request: Request):
    return templates.TemplateResponse("/developer_pages/new_developer.html", {"request": request})

@router.post('', status_code=status.HTTP_201_CREATED, response_class = HTMLResponse)
def createDeveloper(request: Request, db: Session = Depends(get_db), nome_programador: str = Form(...), email: str = Form(...), id_startup: str = Form(...), genero: str = Form(...), data_nascimento: str = Form(...)):
    new_developer = models.Programador(
        id_startup = id_startup,
        nome_programador = nome_programador,
        genero = genero,
        data_nascimento = data_nascimento,
        email = email
    )

    db.add(new_developer)

    db.commit()

    db.refresh(new_developer)

    return getAllDevelopers(request, db)

@router.get('', response_class = HTMLResponse)
def getAllDevelopers(request: Request, db: Session = Depends(get_db)):
    developers = db.query(models.Programador).all()
    return templates.TemplateResponse('/developer_pages/list_developers.html', {'request': request, 'developer_list': developers})

@router.get('/{id}', response_class = HTMLResponse)
def getDeveloper(id, request: Request, db: Session = Depends(get_db)):
    developer = db.query(models.Programador).filter(models.Programador.id_programador == id).first()

    if not developer:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f'The developer with the id {id} is not found')

    developer = developer.__dict__
    developer['data_nascimento'] = str(developer['data_nascimento'].day) + "/" + str(developer['data_nascimento'].month) + "/" + str(developer['data_nascimento'].year)
    return templates.TemplateResponse("/developer_pages/view_developer.html", {"request": request, "developer": developer})

@router.get("/edit/{id}",response_class=HTMLResponse)
def edit_startup(id:int, response:Response, request:Request, db: Session = Depends(get_db)):
    developer = db.query(models.Programador).filter(models.Programador.id_programador == id).first()
    return templates.TemplateResponse("/developer_pages/edit_developer.html", {"request": request, "developer": developer})

@router.post('/update/{id}', status_code = status.HTTP_202_ACCEPTED)
def updateStartup(id, request: Request, db: Session = Depends(get_db), nome_programador:str = Form(...), email:str = Form(...), id_programador:int = Form(...), id_startup:int = Form(...), genero:str = Form(...), data_nascimento:str = Form(...)):
    developer = db.query(models.Programador).filter(models.Programador.id_programador == id)

    if not developer.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f'The developer with the id {id} is not found')

    updatedDeveloper = {
        'id_programador': id_programador,
        'id_startup': id_startup,
        'nome_programador': nome_programador,
        'genero': genero,
        'data_nascimento': data_nascimento,
        'email': email
    }

    developer.update(updatedDeveloper)
    db.commit()

    return getAllDevelopers(request, db)

@router.get('/delete/{id}', status_code = status.HTTP_204_NO_CONTENT, response_class = HTMLResponse)
def deleteStartup(id:int, request: Request, db: Session = Depends(get_db)):
    developer = db.query(models.Programador).filter(models.Programador.id_programador == id)

    if not developer.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f'The startup with the id {id} is not found')

    developer.delete(synchronize_session=False)
    db.commit()
    return getAllDevelopers(request, db)