-- Tabela Alunos
CREATE TABLE Alunos (
    aluno_id SERIAL PRIMARY KEY,
    nome character varying(100),
    endereco character varying(255),
    cidade character varying(100),
    estado character varying(50),
    cep character varying(20),
    pais character varying(50),
    telefone character varying(20)
);

-- Inserir dados 
INSERT INTO Alunos (nome, endereco, cidade, estado, cep, pais, telefone) VALUES
('João Silva', 'Rua das Flores, 123', 'São Paulo', 'SP', '01010-000', 'Brasil', '(11) 91234-5678'),
('Maria Oliveira', 'Av. Brasil, 456', 'Rio de Janeiro', 'RJ', '20000-000', 'Brasil', '(21) 99876-5432'),
('Carlos Souza', 'Rua A, 789', 'Belo Horizonte', 'MG', '30000-000', 'Brasil', '(31) 97654-3210');

