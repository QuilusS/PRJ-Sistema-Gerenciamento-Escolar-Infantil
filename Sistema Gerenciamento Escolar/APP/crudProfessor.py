from flask import Flask, request, jsonify
import Util.bd as bd
import base64

app = Flask(__name__)

@app.route('/professores', methods=['POST'])
def create_professor():
    data = request.get_json()
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Falha ao conectar ao banco"}), 500
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO "Professor" (id_professor, nome_completo, email, telefone)
            VALUES (%s, %s, %s, %s)
            """,
            (data ['id_professor'], data['nome_completo'], data['email'], data['telefone'])
        )
        conn.commit()
        return jsonify({"message": "Professor criado com sucesso"}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()


@app.route('/professores/<int:id_professor>', methods=['GET'])
def read_professor(id_professor):
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Falha ao conectar ao banco"}), 500
    cursor = conn.cursor()
    try:
        cursor.execute("""
        SELECT id_professor, nome_completo, email, telefone
        FROM public."Professor"
        WHERE id_professor = %s;
        """, (id_professor,))
        professor = cursor.fetchone()
        if professor is None:
            return jsonify({"error": "Professor não encontrado"}), 404
        return jsonify({
            "id_professor": professor[0],
            "nome_completo": professor[1],
            "email": professor[2],
            "telefone": professor[3]
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()


@app.route('/professores/<int:id_professor>', methods=['PUT'])
def update_professor(id_professor):
    data = request.get_json()
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Falha ao conectar ao banco"}), 500
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            UPDATE public."Professor"
            SET nome_completo = %s, email = %s, telefone = %s
            WHERE id_professor = %s;
            """,
            (data['nome_completo'], data['email'], data['telefone'], id_professor)
        )
        conn.commit()
        return jsonify({"message": "Professor atualizado com sucesso"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()


@app.route('/professores/<int:id_professor>', methods=['DELETE'])
def delete_professor(id_professor):
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Falha ao conectar ao banco"}), 500
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM public.\"Professor\" WHERE id_professor = %s;", (id_professor,))
        conn.commit()
        return jsonify({"message": "Professor deletado com sucesso"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()
