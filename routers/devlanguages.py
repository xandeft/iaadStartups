from fastapi import APIRouter, Depends, status, HTTPException, Request, Response, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import Optional, List
from sqlalchemy.orm import Session
import schemas, models, database

router = APIRouter(
    prefix = "/programling",
    tags = ['Developers and Languages']
)

get_db = database.get_db

templates = Jinja2Templates(directory="templates")

def getStartupName(id, db: Session = Depends(get_db)):
    startup = db.query(models.Startup).filter(models.Startup.id_startup == id).first()

    if not startup:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f'The startup with the id {id} is not found')

    return startup.__dict__['nome_startup']

def getLanguageName(id, db: Session = Depends(get_db)):
    language = db.query(models.Linguagem_Programacao).filter(models.Linguagem_Programacao.id_linguagem == id).first()

    if not language:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f'The startup with the id {id} is not found')

    return language.__dict__['nome_linguagem']

def getLanguagemID(languageName, db: Session = Depends(get_db)):
    language = db.query(models.Linguagem_Programacao).filter(models.Linguagem_Programacao.nome_linguagem == languageName).first()

    if not language:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f'The language with name {languageName} is not found')

    return language.__dict__['id_linguagem']


def getDeveloperName(id, db: Session = Depends(get_db)):
    developer = db.query(models.Programador).filter(models.Programador.id_programador == id).first()

    if not developer:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f'The developer with the id {id} is not found')

    return developer.__dict__['nome_programador']

def getDevelopers(id, db: Session = Depends(get_db)):
    developer = db.query(models.Programador).filter(models.Programador.id_programador == id).first()

    if not developer:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f'The developer with the id {id} is not found')

    developer = developer.__dict__
    dev = {
        "nome_programador": developer["nome_programador"],
        "id_programador": developer["id_programador"],
        "nome_startup": getStartupName(developer["id_startup"], db),
        "email": developer["email"]
        }

    return dev

@router.get("/createui", response_class=HTMLResponse)
def create_startup_ui(request: Request):
    return templates.TemplateResponse("/devlanguages_pages/new_devlanguages.html", {"request": request})

@router.post('', status_code=status.HTTP_201_CREATED, response_class=HTMLResponse)
def createDevsLanguages(request: Request, db: Session = Depends(get_db), nome_linguagem: str = Form(...), id_programador: int = Form(...)):
    new_insert = models.Programador_Linguagem(id_programador=id_programador, id_linguagem=getLanguagemID(nome_linguagem, db))

    db.add(new_insert)

    db.commit()

    db.refresh(new_insert)

    return getAllDevsLanguages(request, db)

@router.get('', response_class=HTMLResponse)
def getAllDevsLanguages(request: Request, db: Session = Depends(get_db)):
    devsLanguages = db.query(models.Programador_Linguagem)

    if not devsLanguages.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Nothing datas")
    
    devs = []

    for i in devsLanguages.all():
        devs.append(
            {
                'id_linguagem': i.__dict__['id_linguagem'],
                'nome_linguagem': getLanguageName(i.__dict__['id_linguagem'], db),
                'nome_programador': getDeveloperName(i.__dict__['id_programador'], db),
                'id_programador': i.__dict__['id_programador']
            }
        )
    return templates.TemplateResponse('/devlanguages_pages/list_devlanguages.html', {'request': request, 'devsLanguages_list': devs})

@router.get('/delete/{id_linguagem}/{id_programador}', status_code = status.HTTP_204_NO_CONTENT, response_class = HTMLResponse)
def deleteStartup(id_linguagem, id_programador, request: Request, db: Session = Depends(get_db)):
    print(id_linguagem, id_programador)
    devsLanguages = db.query(models.Programador_Linguagem).filter(models.Programador_Linguagem.id_linguagem == id_linguagem and models.Programador_Linguagem.id_programador == id_programador)

    if not devsLanguages.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f'The startup with the id {id} is not found')

    devsLanguages.delete(synchronize_session=False)
    db.commit()

    return getAllDevsLanguages(request, db)

