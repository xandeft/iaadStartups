from typing import Optional
from fastapi import APIRouter, Depends, status, HTTPException, Request, Response, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import schemas, models, database

router = APIRouter(
    prefix = "/linguagemprog",
    tags = ['Program Languages']
)

get_db = database.get_db

templates = Jinja2Templates(directory="templates")


def getDeveloperName(id, db: Session = Depends(get_db)):
    developer = db.query(models.Programador).filter(models.Programador.id_programador == id).first()

    if not developer:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f'The developer with the id {id} is not found')

    return developer.__dict__['nome_programador']

def getDevsOfLanguage(id_linguagem, db: Session = Depends(get_db)):
    developer = db.query(models.Programador_Linguagem).filter(models.Programador_Linguagem.id_linguagem == id_linguagem)

    devs = []

    if not developer.first():
        return []
        #raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f'The developer with the id {id} is not found')

    for i in developer.all():

        devs.append(getDeveloperName(i.__dict__['id_programador'], db))

    return devs

def getLanguageData(id_linguagem, db: Session = Depends(get_db)):
    languageData = db.query(models.Programador_Linguagem).filter(models.Programador_Linguagem.id_linguagem == id_linguagem)

    if languageData.first():
        return True
    
    return False

@router.get("/createui", response_class=HTMLResponse)
def create_startup_ui(request: Request):
    return templates.TemplateResponse("/language_pages/new_language.html", {"request": request})

@router.post('', status_code=status.HTTP_201_CREATED, response_class=HTMLResponse)
def createStartup(request: Request, db: Session = Depends(get_db), nome_linguagem: str = Form(...), ano_lancamento:str = Form(...)):
    new_language = models.Linguagem_Programacao(nome_linguagem=nome_linguagem, ano_lancamento=ano_lancamento)

    db.add(new_language)

    db.commit()

    db.refresh(new_language)

    return getAllLanguages(request, db)

@router.get('', response_class=HTMLResponse)
def getAllLanguages(request: Request, db: Session = Depends(get_db), onDelete: Optional[int] = None):
    languages = db.query(models.Linguagem_Programacao).all()
    return templates.TemplateResponse('/language_pages/list_languages.html', {'request': request, 'language_list': languages, 'onDelete': onDelete})

@router.get('/{id}')
def getLanguage(id, request: Request, db: Session = Depends(get_db)):
    language = db.query(models.Linguagem_Programacao).filter(models.Linguagem_Programacao.id_linguagem == id).first()

    if not language:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f'The startup with the id {id} is not found')

    language = language.__dict__
    devs = getDevsOfLanguage(language['id_linguagem'], db)
    language["devs"] = devs
    language["lenDevs"] = len(devs)

    return templates.TemplateResponse("/language_pages/view_language.html", {"request": request, "language": language})

@router.get("/edit/{id}", response_class=HTMLResponse)
def editLanguage(id:int, response:Response, request:Request, db: Session = Depends(get_db)):
    language = db.query(models.Linguagem_Programacao).filter(models.Linguagem_Programacao.id_linguagem == id).first()
    return templates.TemplateResponse("/language_pages/edit_language.html", {"request": request, "language": language})


@router.post('/update/{id}', status_code = status.HTTP_202_ACCEPTED, response_class=HTMLResponse)
def updateStartup(id: int, response: Response, request: Request, db: Session = Depends(get_db), id_linguagem:int = Form(...), nome_linguagem: str = Form(...), ano_lancamento: str = Form(...)):
    language = db.query(models.Linguagem_Programacao).filter(models.Linguagem_Programacao.id_linguagem == id)

    if not language.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f'The startup with the id {id} is not found')

    updatedLanguage = {
        'id_linguagem': id_linguagem,
        'nome_linguagem': nome_linguagem,
        'ano_lancamento': ano_lancamento
    }

    language.update(updatedLanguage)
    db.commit()

    return getAllLanguages(request, db)

@router.get('/delete/{id}', status_code = status.HTTP_204_NO_CONTENT, response_class = HTMLResponse)
def deleteStartup(id, request: Request, db: Session = Depends(get_db)):
    language = db.query(models.Linguagem_Programacao).filter(models.Linguagem_Programacao.id_linguagem == id)

    if not language.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f'The startup with the id {id} is not found')

    checkLanguageData = getLanguageData(id, db)

    try:
        language.delete(synchronize_session=False)
        db.commit()
        return getAllLanguages(request, db)
    except:
        return getAllLanguages(request, db, checkLanguageData)