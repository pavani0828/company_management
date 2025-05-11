from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect("company.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    conn = get_db_connection()
    companies = conn.execute("SELECT * FROM companies").fetchall()
    conn.close()
    return render_template("index.html", companies=companies)

@app.route("/add", methods=["POST"])
def add():
    name = request.form["name"]
    location = request.form["location"]
    conn = get_db_connection()
    conn.execute("INSERT INTO companies (name, location) VALUES (?, ?)", (name, location))
    conn.commit()
    conn.close()
    return redirect("/")

@app.route("/delete/<int:company_id>")
def delete(company_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM companies WHERE id = ?", (company_id,))
    conn.commit()
    conn.close()
    return redirect("/")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
