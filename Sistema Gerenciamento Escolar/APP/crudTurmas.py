from flask import Flask, request, jsonify
import Util.bd as bd
import base64

app = Flask(__name__)

@app.route('/turmas', methods=['POST'])
def create_turma():
    data = request.get_json()
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Falha ao conectar ao banco"}), 500
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO "Turma" (id_turma, nome_turma, id_professor, horario)
            VALUES (%s, %s, %s, %s)
            """,
            (data ['id_turma'], data['nome_turma'], data['id_professor'], data['horario'])
        )
        conn.commit()
        return jsonify({"message": "Turma criada com sucesso"}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()


@app.route('/turmas/<int:id_turma>', methods=['GET'])
def read_turma(id_turma):
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Falha ao conectar ao banco"}), 500
    cursor = conn.cursor()
    try:
        cursor.execute("""
        SELECT id_turma, nome_turma, id_professor, horario
        FROM public."Turma"
        WHERE id_turma = %s;
        """, (id_turma,))
        turma = cursor.fetchone()
        if turma is None:
            return jsonify({"error": "Turma não encontrada"}), 404
        return jsonify({
            "id_turma": turma[0],
            "nome_turma": turma[1],
            "id_professor": turma[2],
            "horario": turma[3]
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()


@app.route('/turmas/<int:id_turma>', methods=['PUT'])
def update_turma(id_turma):
    data = request.get_json()
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Falha ao conectar ao banco"}), 500
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            UPDATE public."Turma"
            SET nome_turma = %s, id_professor = %s, horario = %s
            WHERE id_turma = %s;
            """,
            (data['nome_turma'], data['id_professor'], data['horario'], id_turma)
        )
        conn.commit()
        return jsonify({"message": "Turma atualizada com sucesso"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()


@app.route('/turmas/<int:id_turma>', methods=['DELETE'])
def delete_turma(id_turma):
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Falha ao conectar ao banco"}), 500
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM public.\"Turma\" WHERE id_turma = %s;", (id_turma,))
        conn.commit()
        return jsonify({"message": "Turma deletada com sucesso"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()