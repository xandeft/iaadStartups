from pydantic import BaseModel
from typing import List

class BaseStartup(BaseModel):
    id_startup: int
    nome_startup: str
    cidade_sede: str

class CreateStartup(BaseModel):
    nome_startup: str
    cidade_sede: str

    class Config():
        orm_mode = True

class UpdateStartup(BaseModel):
    nome_startup: str
    cidade_sede: str

    class Config():
        orm_mode = True

class showProgramador(BaseModel):
    id_programador: int
    nome_programador: str
    id_startup: int

    class Config():
        orm_mode = True

class showStartup(BaseModel):
    nome_startup: str
    cidade_sede: str

    class Config():
        orm_mode = True

class BaseProgramador(BaseModel):
    id_programador: int
    id_startup: int
    nome_programador: str
    genero: str
    data_nascimento: str
    email: str

class CreateProgramador(BaseModel):
    id_startup: int
    nome_programador: str
    genero: str
    data_nascimento: str
    email: str

    class Config():
        orm_mode = True

class UpdateProgramador(BaseModel):
    id_startup: int
    nome_programador: str
    genero: str
    data_nascimento: str
    email: str

    class Config():
        orm_mode = True

class Linguagem_Programacao(BaseModel):
    id_linguagem: int
    nome_linguagem: str
    ano_lancamento: str

class CreateLinguagem_Programacao(BaseModel):
    nome_linguagem: str
    ano_lancamento: str

    class Config():
        orm_mode = True

class UpdateLinguagem_Programacao(BaseModel):
    nome_linguagem: str
    ano_lancamento: str

    class Config():
        orm_mode = True

class Programador_Linguagem(BaseModel):
    id_programador: int
    id_linguagem: int