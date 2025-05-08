from flask import Flask, request, jsonify
from flasgger import Swagger
from prometheus_flask_exporter import PrometheusMetrics
from prometheus_client import Counter
import Util.bd as bd
import logging
import psycopg2
from error_handler import handle_db_error, handle_application_error

# Configuração do logging
logging.basicConfig(
    filename="escola_infantil.log",
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(message)s"
)
logger = logging.getLogger()

app = Flask(__name__)

# Configuração do Swagger
swagger = Swagger(app)

# Configuração do Prometheus
metrics = PrometheusMetrics(app, default_labels={'app_name': 'escola_infantil_app'})

# Métricas personalizadas para sucessos e erros
success_counter = Counter(
    'http_success_count', 'Contagem de respostas HTTP com sucesso',
    ['endpoint', 'method', 'status']
)

error_counter = Counter(
    'http_error_count', 'Contagem de respostas HTTP com erro',
    ['endpoint', 'method', 'status']
)

@app.after_request
def after_request(response):
    """
    Middleware para capturar os retornos de todos os endpoints.
    """
    endpoint = request.path
    method = request.method
    status = response.status_code

    if 200 <= status < 300:
        success_counter.labels(endpoint=endpoint, method=method, status=str(status)).inc()
    else:
        error_counter.labels(endpoint=endpoint, method=method, status=str(status)).inc()

    return response

@app.route('/alunos', methods=['POST'])
def create_aluno():
    data = request.get_json()
    conn = bd.create_connection()
    if conn is None:
        logger.error("CREATE - Falha na conexão com o banco de dados.")
        return jsonify({"error": "Falha ao conectar ao banco"}), 500

    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO "Alunos" (nome, endereco, cidade, estado, cep, pais, telefone)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (data['nome'], data.get('endereco'), data.get('cidade'), data.get('estado'), 
             data.get('cep'), data.get('pais'), data.get('telefone'))
        )
        conn.commit()
        logger.info(f"CREATE - Aluno Nome: {data['nome']} - Status: SUCESSO")
        return jsonify({"message": "Aluno criado com sucesso"}), 201
    except Exception as e:
        conn.rollback()
        return handle_db_error(e, "CREATE")
    finally:
        cursor.close()
        conn.close()

@app.route('/alunos/<int:aluno_id>', methods=['GET'])
def read_aluno(aluno_id):
    conn = bd.create_connection()
    if conn is None:
        logger.error("READ - Falha na conexão com o banco de dados.")
        return jsonify({"error": "Falha ao conectar ao banco"}), 500
    
    cursor = conn.cursor()
    try:
        cursor.execute("""
        SELECT aluno_id, nome, endereco, cidade, estado, cep, pais, telefone
        FROM public."Alunos"
        WHERE aluno_id = %s;
        """, (aluno_id,))
        aluno = cursor.fetchone()
        if aluno is None:
            logger.warning(f"READ - Aluno ID: {aluno_id} - Status: NÃO ENCONTRADO")
            return jsonify({"error": "Aluno não encontrado"}), 404

        logger.info(f"READ - Aluno ID: {aluno_id}, Nome: {aluno[1]} - Status: SUCESSO")
        return jsonify({
            "aluno_id": aluno[0],
            "nome": aluno[1],
            "endereco": aluno[2],
            "cidade": aluno[3],
            "estado": aluno[4],
            "cep": aluno[5],
            "pais": aluno[6],
            "telefone": aluno[7]
        }), 200
    except Exception as e:
        return handle_db_error(e, "READ", aluno_id)
    finally:
        cursor.close()
        conn.close()

@app.route('/alunos/<int:aluno_id>', methods=['PUT'])
def update_aluno(aluno_id):
    data = request.get_json()
    conn = bd.create_connection()
    if conn is None:
        logger.error("UPDATE - Falha na conexão com o banco de dados.")
        return jsonify({"error": "Falha ao conectar ao banco"}), 500
    
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            UPDATE public."Alunos"
            SET nome = %s, endereco = %s, cidade = %s, estado = %s, 
                cep = %s, pais = %s, telefone = %s
            WHERE aluno_id = %s;
            """,
            (data['nome'], data.get('endereco'), data.get('cidade'), data.get('estado'), 
             data.get('cep'), data.get('pais'), data.get('telefone'), aluno_id)
        )
        conn.commit()
        logger.info(f"UPDATE - Aluno ID: {aluno_id}, Nome: {data['nome']} - Status: SUCESSO")
        return jsonify({"message": "Aluno atualizado com sucesso"}), 200
    except Exception as e:
        conn.rollback()
        return handle_db_error(e, "UPDATE", aluno_id)
    finally:
        cursor.close()
        conn.close()

@app.route('/alunos/<int:aluno_id>', methods=['DELETE'])
def delete_aluno(aluno_id):
    conn = bd.create_connection()
    if conn is None:
        logger.error("DELETE - Falha na conexão com o banco de dados.")
        return jsonify({"error": "Falha ao conectar ao banco"}), 500
    
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM public."Alunos" WHERE aluno_id = %s;", (aluno_id,))
        conn.commit()
        logger.info(f"DELETE - Aluno ID: {aluno_id} - Status: SUCESSO")
        return jsonify({"message": "Aluno deletado com sucesso"}), 200
    except Exception as e:
        conn.rollback()
        return handle_db_error(e, "DELETE", aluno_id)
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
