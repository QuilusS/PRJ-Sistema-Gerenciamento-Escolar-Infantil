# Sistema de Gerenciamento Escolar - Banco de Dados

Este projeto utiliza o PostgreSQL como banco de dados para o sistema de gerenciamento escolar. Abaixo estão as instruções para configurar e utilizar o ambiente Docker para o banco de dados.

---

## Estrutura do Dockerfile

```dockerfile
# Use a imagem oficial do PostgreSQL como base
FROM postgres:latest

# Defina variáveis de ambiente para configurar o PostgreSQL
ENV POSTGRES_DB=mydatabase
ENV POSTGRES_USER=myuser
ENV POSTGRES_PASSWORD=mypassword

# Copie o script de inicialização para o diretório de inicialização do PostgreSQL
COPY init.sql /docker-entrypoint-initdb.d/

# Exponha a porta padrão do PostgreSQL
EXPOSE 5432
```

---

## Como Utilizar

### Passo 1: Construir a Imagem Docker
Para construir a imagem Docker, execute o seguinte comando no diretório onde o `Dockerfile` está localizado:

```bash
docker build -t my-postgres-image .
```

### Passo 2: Executar o Contêiner
Para executar o contêiner Docker com a imagem criada, utilize o seguinte comando:

```bash
docker run -d --name my-postgres-container -p 2000:5432 my-postgres-image
```

### Passo 3: Conectar ao PostgreSQL
Você pode se conectar ao PostgreSQL utilizando um cliente PostgreSQL, como **DBeaver**, **psql**, ou qualquer ferramenta de gerenciamento de banco de dados que suporte PostgreSQL. Utilize as seguintes credenciais:

- **Host:** `localhost`
- **Porta:** `2000`
- **Banco de Dados:** `Escola`
- **Usuário:** `faat`
- **Senha:** `faat`

---

## Observações

- Certifique-se de que a porta `2000` não esteja sendo utilizada por outro serviço no seu sistema.
- O arquivo `init.sql` deve conter os scripts necessários para inicializar o banco de dados com as tabelas e dados necessários para o sistema.

---

## Recursos Adicionais

- [Documentação Oficial do PostgreSQL](https://www.postgresql.org/docs/)
- [Documentação do Docker](https://docs.docker.com/)

---

## Problemas Comuns

### Erro: Porta já está em uso
Se você receber um erro indicando que a porta `2000` já está em uso, altere a porta no comando `docker run` para uma disponível no seu sistema. Por exemplo:

```bash
docker run -d --name my-postgres-container -p 3000:5432 my-postgres-image
```

### Erro: Conexão recusada
Certifique-se de que o contêiner está em execução e que você está utilizando as credenciais corretas.

---

Com essas instruções, você deve conseguir configurar e utilizar o banco de dados PostgreSQL para o sistema de gerenciamento escolar com facilidade.


