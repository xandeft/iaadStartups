from sqlalchemy import Column, ForeignKey, String, Integer
from sqlalchemy.orm import relationship
from database import Base

class Startup(Base):
    __tablename__ = "Startup"
    id_startup = Column(Integer, primary_key=True, index = True)
    nome_startup = Column(String)
    cidade_sede = Column(String)


class Programador(Base):
    __tablename__ = "Programador"
    id_programador = Column(Integer, primary_key=True)
    id_startup = Column(Integer, ForeignKey('Startup.id_startup'))
    nome_programador = Column(String)
    genero = Column(String)
    data_nascimento = Column(String)
    email = Column(String)

    
class Linguagem_Programacao(Base):
    __tablename__ = "Linguagem_Programacao"
    id_linguagem = Column(Integer, primary_key=True)
    nome_linguagem = Column(String)
    ano_lancamento = Column(String)

class Programador_Linguagem(Base):
    __tablename__ = "Programador_Linguagem"
    id_programador = Column(Integer, ForeignKey('Programador.id_programador'), primary_key=True)
    id_linguagem = Column(Integer, ForeignKey('Linguagem_Programacao.id_linguagem'), primary_key=True)
