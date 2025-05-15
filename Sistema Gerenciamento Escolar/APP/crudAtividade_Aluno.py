@app.route('/atividade_aluno', methods=['POST'])
def create_atividade_aluno():
    data = request.get_json()
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Falha ao conectar ao banco"}), 500
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO "Atividade_Aluno" (id_atividade, id_aluno)
            VALUES (%s, %s)
            """,
            (data['id_atividade'], data['id_aluno'])
        )
        conn.commit()
        return jsonify({"message": "Ligação entre Atividade e Aluno criada com sucesso"}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()


@app.route('/atividade_aluno/<int:id_atividade>/<int:id_aluno>', methods=['GET'])
def read_atividade_aluno(id_atividade, id_aluno):
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Falha ao conectar ao banco"}), 500
    cursor = conn.cursor()
    try:
        cursor.execute("""
        SELECT id_atividade, id_aluno
        FROM public."Atividade_Aluno"
        WHERE id_atividade = %s AND id_aluno = %s;
        """, (id_atividade, id_aluno))
        atividade_aluno = cursor.fetchone()
        if atividade_aluno is None:
            return jsonify({"error": "Ligação entre Atividade e Aluno não encontrada"}), 404
        return jsonify({
            "id_atividade": atividade_aluno[0],
            "id_aluno": atividade_aluno[1]
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()


@app.route('/atividade_aluno/<int:id_atividade>/<int:id_aluno>', methods=['DELETE'])
def delete_atividade_aluno(id_atividade, id_aluno):
    conn = bd.create_connection()
    if conn is None:
        return jsonify({"error": "Falha ao conectar ao banco"}), 500
    cursor = conn.cursor()
    try:
        cursor.execute("""
        DELETE FROM public."Atividade_Aluno"
        WHERE id_atividade = %s AND id_aluno = %s;
        """, (id_atividade, id_aluno))
        conn.commit()
        return jsonify({"message": "Ligação entre Atividade e Aluno removida com sucesso"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()