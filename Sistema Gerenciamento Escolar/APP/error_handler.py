import logging
import psycopg2

# Configuração do logging para erros
logging.basicConfig(
    filename="escola_infantil.log",
    level=logging.ERROR,
    format="%(asctime)s - [%(levelname)s] - %(message)s"
)
logger = logging.getLogger()

def handle_db_error(error, operacao, aluno_id=None):
    """Captura e registra erros do banco de dados, retornando mensagens padronizadas"""
    mensagem_erro = f"{operacao} - Aluno ID: {aluno_id if aluno_id else 'N/A'} - ERRO SQL: {str(error)}"
    logger.error(mensagem_erro)

    if isinstance(error, psycopg2.errors.UniqueViolation):
        return {"error": "Este aluno já está cadastrado. Verifique os dados."}, 400
    elif isinstance(error, psycopg2.errors.ForeignKeyViolation):
        return {"error": "Erro de integridade: referência inválida."}, 400
    elif isinstance(error, psycopg2.errors.SyntaxError):
        return {"error": "Erro de sintaxe na consulta SQL."}, 500
    else:
        return {"error": "Erro interno no banco de dados."}, 500

def handle_application_error(error, operacao):
    """Captura e registra erros da aplicação"""
    mensagem_erro = f"{operacao} - ERRO: {str(error)}"
    logger.error(mensagem_erro)
    return {"error": "Erro inesperado na aplicação. Contate o suporte."}, 500
