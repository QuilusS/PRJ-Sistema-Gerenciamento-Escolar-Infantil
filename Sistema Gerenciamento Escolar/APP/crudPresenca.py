from flask import Flask, request, jsonify
import Util.bd as bd
import base64

app = Flask(__name__)

@app.route('/presencas', methods=['POST'])
def create_presenca():
    data = request.get_json()
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Falha ao conectar ao banco"}), 500
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO "Presenca" (id_presenca, id_aluno, data_presenca, presente)
            VALUES (%s, %s, %s, %s)
            """,
            (data ['id_presenca'], data['id_aluno'], data['data_presenca'], data['presente'])
        )
        conn.commit()
        return jsonify({"message": "Presença registrada com sucesso"}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()


@app.route('/presencas/<int:id_presenca>', methods=['GET'])
def read_presenca(id_presenca):
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Falha ao conectar ao banco"}), 500
    cursor = conn.cursor()
    try:
        cursor.execute("""
        SELECT id_presenca, id_aluno, data_presenca, presente
        FROM public."Presenca"
        WHERE id_presenca = %s;
        """, (id_presenca,))
        presenca = cursor.fetchone()
        if presenca is None:
            return jsonify({"error": "Presença não encontrada"}), 404
        return jsonify({
            "id_presenca": presenca[0],
            "id_aluno": presenca[1],
            "data_presenca": presenca[2],
            "presente": presenca[3]
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()


@app.route('/presencas/<int:id_presenca>', methods=['PUT'])
def update_presenca(id_presenca):
    data = request.get_json()
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Falha ao conectar ao banco"}), 500
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            UPDATE public."Presenca"
            SET id_aluno = %s, data_presenca = %s, presente = %s
            WHERE id_presenca = %s;
            """,
            (data['id_aluno'], data['data_presenca'], data['presente'], id_presenca)
        )
        conn.commit()
        return jsonify({"message": "Presença atualizada com sucesso"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()


@app.route('/presencas/<int:id_presenca>', methods=['DELETE'])
def delete_presenca(id_presenca):
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Falha ao conectar ao banco"}), 500
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM public.\"Presenca\" WHERE id_presenca = %s;", (id_presenca,))
        conn.commit()
        return jsonify({"message": "Presença excluída com sucesso"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()