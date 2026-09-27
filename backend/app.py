from flask import Flask, request, jsonify
from flask_cors import CORS
import ast
import sqlite3

app = Flask(__name__)

CORS(app)


def init_db():

    connection = sqlite3.connect("calculator.db")

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS calculations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            expression TEXT NOT NULL,
            result TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT (datetime('now', 'localtime'))
        )
    """)

    connection.commit()
    connection.close()


def safe_calculate(expression):

    tree = ast.parse(expression, mode="eval")

    allowed_operators = (
        ast.Add,
        ast.Sub,
        ast.Mult,
        ast.Div,
        ast.Mod,
    )

    for node in ast.walk(tree):

        if isinstance(node, ast.BinOp):

            if not isinstance(node.op, allowed_operators):
                raise ValueError("Operator not allowed")

        elif isinstance(node, (ast.Expression, ast.Constant)):

            continue

        elif isinstance(node, allowed_operators):

            continue

        else:

            raise ValueError("Invalid expression")

    return eval(compile(tree, "", "eval"))


@app.route("/")
def home():

    return "Calculator Backend is Running!"


@app.route("/calculate", methods=["POST"])
def calculate():

    try:

        data = request.json
        expression = data["expression"]

        result = safe_calculate(expression)

        connection = sqlite3.connect("calculator.db")
        cursor = connection.cursor()

        cursor.execute(
            "INSERT INTO calculations (expression, result) VALUES (?, ?)",
            (expression, str(result))
        )

        connection.commit()
        connection.close()

        return jsonify({"result": result})

    except ValueError as error:

        return jsonify({"error": str(error)}), 400

@app.route("/history")
def history():

    connection = sqlite3.connect("calculator.db")
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM calculations ORDER BY id DESC"
    )

    calculations = cursor.fetchall()

    connection.close()

    return jsonify(calculations)

@app.route("/clear-history", methods=["DELETE"])
def clear_history():

    connection = sqlite3.connect("calculator.db")
    cursor = connection.cursor()

    cursor.execute("DELETE FROM calculations")

    connection.commit()
    connection.close()

    return jsonify({
        "message": "History cleared successfully"
    })

init_db()
if __name__ == "__main__":
    app.run(debug=True)