import logging

# Configuração do logging para salvar mensagens no arquivo escola_infantil.log
logging.basicConfig(
    filename="escola_infantil.log",
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(message)s"
)
logger = logging.getLogger()

def log_event(operacao, aluno_id=None, nome=None, status="SUCESSO", erro=None):
    """Função para registrar eventos no log com informações contextuais."""
    mensagem = f"{operacao} - ID: {aluno_id if aluno_id else 'N/A'}, Nome: {nome if nome else 'N/A'} - Status: {status}"
    if erro:
        mensagem += f" - ERRO: {erro}"
        logger.error(mensagem)
    else:
        logger.info(mensagem)
