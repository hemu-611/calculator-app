#!/usr/bin/env python3
from flask import Flask, jsonify, render_template, request

from calculator import Calculator, History

app = Flask(__name__)

calculator = Calculator()
history = History()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/calculate", methods=["POST"])
def calculate():
    expr = request.json.get("expr", "").strip()
    if not expr:
        return jsonify({"error": "Empty expression"}), 400
    try:
        value = calculator.evaluate(expr)
        result = calculator.format_result(value)
        history.add(expr, result)
        return jsonify({"result": result})
    except ZeroDivisionError:
        return jsonify({"error": "Division by zero"}), 400
    except (SyntaxError, TypeError):
        return jsonify({"error": "Invalid expression"}), 400
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    except NameError as exc:
        return jsonify({"error": f"{exc}"}), 400
    except Exception as exc:
        return jsonify({"error": str(exc)}), 400


@app.route("/history", methods=["GET"])
def get_history():
    return jsonify(history.entries())


@app.route("/history", methods=["DELETE"])
def clear_history():
    history.clear()
    return jsonify({"ok": True})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
