from flask import Flask, request, jsonify
import Util.bd as bd
import base64

app = Flask(__name__)

@app.route('/pagamentos', methods=['POST'])
def create_pagamento():
    data = request.get_json()
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Falha ao conectar ao banco"}), 500
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO "Pagamento" (id_pagamento, id_aluno, data_pagamento, valor_pago, forma_pagamento, referencia, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (data ['id_pagamento'], data['id_aluno'], data['data_pagamento'], data['valor_pago'], data['forma_pagamento'], 
             data['referencia'], data['status'])
        )
        conn.commit()
        return jsonify({"message": "Pagamento registrado com sucesso"}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()


@app.route('/pagamentos/<int:id_pagamento>', methods=['GET'])
def read_pagamento(id_pagamento):
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Falha ao conectar ao banco"}), 500
    cursor = conn.cursor()
    try:
        cursor.execute("""
        SELECT id_pagamento, id_aluno, data_pagamento, valor_pago, forma_pagamento, referencia, status
        FROM public."Pagamento"
        WHERE id_pagamento = %s;
        """, (id_pagamento,))
        pagamento = cursor.fetchone()
        if pagamento is None:
            return jsonify({"error": "Pagamento não encontrado"}), 404
        return jsonify({
            "id_pagamento": pagamento[0],
            "id_aluno": pagamento[1],
            "data_pagamento": pagamento[2],
            "valor_pago": pagamento[3],
            "forma_pagamento": pagamento[4],
            "referencia": pagamento[5],
            "status": pagamento[6]
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()


@app.route('/pagamentos/<int:id_pagamento>', methods=['PUT'])
def update_pagamento(id_pagamento):
    data = request.get_json()
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Falha ao conectar ao banco"}), 500
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            UPDATE public."Pagamento"
            SET id_aluno = %s, data_pagamento = %s, valor_pago = %s, forma_pagamento = %s, 
                referencia = %s, status = %s
            WHERE id_pagamento = %s;
            """,
            (data['id_aluno'], data['data_pagamento'], data['valor_pago'], data['forma_pagamento'], 
             data['referencia'], data['status'], id_pagamento)
        )
        conn.commit()
        return jsonify({"message": "Pagamento atualizado com sucesso"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()


@app.route('/pagamentos/<int:id_pagamento>', methods=['DELETE'])
def delete_pagamento(id_pagamento):
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Falha ao conectar ao banco"}), 500
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM public.\"Pagamento\" WHERE id_pagamento")