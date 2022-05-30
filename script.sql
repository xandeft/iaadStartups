-- Introdução ao Armazenamento e Análise de Dados (IAAD) - BSI/UFRPE
begin;
create schema Startups;

use Startups;

-- Criando as tabelas
create table Startup(
	id_startup INT NOT NULL AUTO_INCREMENT,
	nome_startup VARCHAR (45),
	cidade_sede VARCHAR (20),
	PRIMARY KEY(id_startup));
    
create table Linguagem_Programacao(
	id_linguagem INT NOT NULL AUTO_INCREMENT,
	nome_linguagem VARCHAR(15),
	ano_lancamento VARCHAR(4),
	PRIMARY KEY (id_linguagem));
    
create table Programador(
	id_programador INT NOT NULL AUTO_INCREMENT,
	id_startup INT,
    nome_programador VARCHAR(45),
    genero CHAR(1),
    data_nascimento DATE NOT NULL,
    email VARCHAR(30) NOT NULL,
	PRIMARY KEY (id_programador),
    UNIQUE(email));
    
create table Programador_Linguagem(
	id_programador INT,
	id_linguagem INT);
    
-- populando/carregando as tabelas do banco de dados
insert into Startup(nome_startup, cidade_sede) values
	('Tech4Toy','Porto Alegre'),
    ('Smart123','Belo Horizonte'),
    ('knowledgeUp','Rio de Janeiro'),
    ('BSI Next Level','Recife'),
    ('QualiHealth','São Paulo'),
    ('ProEdu','Florianópolis');
    
 insert into Linguagem_Programacao(nome_linguagem, ano_lancamento)values
	('Python', '1991'),
    ('PHP', '1995'),
    ('Java', '1995'),
    ('C', '1972'),
    ('JavaScript', '1995'),
    ('Dart', '2011');
    
insert into Programador(id_startup, nome_programador, genero, data_nascimento, email)values
	('1','João Pedro', 'M','1993-06-23', 'joaop@mail.com'),
    ('2','Paula Silva', 'F','1986-01-10', 'paulas@mail.com'),
    ('3','Renata Vieira', 'F','1991-07-05', 'renatav@mail.com'),
    ('4','Felipe Santos', 'M','1976-11-25', 'felipes@mail.com'),
    ('1','Ana Cristina', 'F','1968-02-19', 'anac@mail.com'),
    ('4','Alexandre Alves', 'M','1988-07-07', 'alexandrea@mail.com'),
    ('2','Laura Marques', 'F','1987-10-04', 'lauram@mail.com');
    
insert into Programador_Linguagem values
	('1', '1'),
    ('1', '2'),
    ('2', '3'),
    ('3', '4'),
    ('3', '5'),
    ('4', '5'),
    ('7', '1'),
    ('7', '2');


-- Aplicando a restrição de integridade referencial (chaves estrangeiras - FK) e ações de disparo referencial
alter table Programador	ADD FOREIGN KEY(id_startup) REFERENCES Startup(id_startup) ON UPDATE CASCADE;
alter table Programador_Linguagem ADD FOREIGN KEY(id_programador) REFERENCES Programador(id_programador) ON DELETE CASCADE;
alter table Programador_Linguagem ADD FOREIGN KEY(id_linguagem) REFERENCES Linguagem_Programacao(id_linguagem) ON DELETE RESTRICT;
commit;