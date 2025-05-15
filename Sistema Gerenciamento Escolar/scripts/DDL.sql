-- Script DDL para Sistema de Gestão Escolar Simplificado
-- Dialeto: PostgreSQL

-- Tabela Professor (deve vir primeiro por causa das referências)
CREATE TABLE Professor (
  id_professor SERIAL PRIMARY KEY,
  nome_completo VARCHAR(255) NOT NULL,
  email VARCHAR(100),
  telefone VARCHAR(20)
);

-- Tabela Turma
CREATE TABLE Turma (
  id_turma SERIAL PRIMARY KEY,
  nome_turma VARCHAR(50) NOT NULL,
  id_professor INTEGER REFERENCES Professor(id_professor),
  horario VARCHAR(100)
);

-- Tabela Aluno
CREATE TABLE Aluno (
  id_aluno SERIAL PRIMARY KEY,
  nome_completo VARCHAR(255) NOT NULL,
  data_nascimento DATE,
  id_turma INTEGER REFERENCES Turma(id_turma),
  nome_responsavel VARCHAR(255) NOT NULL,
  telefone_responsavel VARCHAR(20) NOT NULL,
  email_responsavel VARCHAR(100),
  informacoes_adicionais TEXT
);

-- Tabela Pagamento
CREATE TABLE Pagamento (
  id_pagamento SERIAL PRIMARY KEY,
  id_aluno INTEGER NOT NULL REFERENCES Aluno(id_aluno),
  data_pagamento DATE NOT NULL,
  valor_pago DECIMAL(10, 2) NOT NULL,
  forma_pagamento VARCHAR(50) NOT NULL,
  referencia VARCHAR(100) NOT NULL,
  status VARCHAR(20) NOT NULL
);

-- Tabela Presenca
CREATE TABLE Presenca (
  id_presenca SERIAL PRIMARY KEY,
  id_aluno INTEGER NOT NULL REFERENCES Aluno(id_aluno),
  data_presenca DATE NOT NULL,
  presente BOOLEAN NOT NULL DEFAULT TRUE
);

-- Tabela Atividade
CREATE TABLE Atividade (
  id_atividade SERIAL PRIMARY KEY,
  descricao TEXT NOT NULL,
  data_realizacao DATE NOT NULL
);

-- Tabela de ligação Atividade_Aluno (N:N)
CREATE TABLE Atividade_Aluno (
  id_atividade INTEGER NOT NULL REFERENCES Atividade(id_atividade),
  id_aluno INTEGER NOT NULL REFERENCES Aluno(id_aluno),
  PRIMARY KEY (id_atividade, id_aluno)
);

-- Tabela Usuario
CREATE TABLE Usuario (
  id_usuario SERIAL PRIMARY KEY,
  login VARCHAR(50) NOT NULL UNIQUE,
  senha VARCHAR(255) NOT NULL,
  nivel_acesso VARCHAR(20) NOT NULL,
  id_professor INTEGER REFERENCES Professor(id_professor)
);

-- Índices para melhorar performance
CREATE INDEX idx_aluno_turma ON Aluno(id_turma);
CREATE INDEX idx_turma_professor ON Turma(id_professor);
CREATE INDEX idx_pagamento_aluno ON Pagamento(id_aluno);
CREATE INDEX idx_presenca_aluno ON Presenca(id_aluno);
CREATE INDEX idx_atividade_aluno ON Atividade_Aluno(id_aluno);
CREATE INDEX idx_usuario_professor ON Usuario(id_professor);