from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

DATABASE = "employee.db"


# ---------------- DATABASE ----------------

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def create_database():

    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            department TEXT NOT NULL,
            salary TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# Create database when app starts
create_database()


# ---------------- HOME ----------------

@app.route("/")
def home():

    conn = get_db()

    total_employees = conn.execute(
        "SELECT COUNT(*) FROM employees"
    ).fetchone()[0]

    conn.close()

    return render_template(
        "index.html",
        total_employees=total_employees
    )


# ---------------- ADD EMPLOYEE ----------------

@app.route("/add", methods=["GET", "POST"])
def add_employee():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        department = request.form["department"]
        salary = request.form["salary"]

        conn = get_db()

        conn.execute("""
            INSERT INTO employees
            (name, email, phone, department, salary)
            VALUES (?, ?, ?, ?, ?)
        """, (
            name,
            email,
            phone,
            department,
            salary
        ))

        conn.commit()
        conn.close()

        return redirect("/employees")

    return render_template("add_employee.html")


# ---------------- VIEW EMPLOYEES ----------------

@app.route("/employees")
def employees():

    conn = get_db()

    employees = conn.execute(
        "SELECT * FROM employees"
    ).fetchall()

    conn.close()

    return render_template(
        "employees.html",
        employees=employees
    )


# ---------------- DELETE EMPLOYEE ----------------

@app.route("/delete/<int:id>")
def delete_employee(id):

    conn = get_db()

    conn.execute(
        "DELETE FROM employees WHERE id = ?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/employees")


# ---------------- RUN ----------------

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
