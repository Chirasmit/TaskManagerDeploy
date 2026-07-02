from flask import Flask, render_template, request, redirect, session, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = "taskmanager123"


db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="taskman"
)

cursor = db.cursor()


@app.route("/")
def home():

    if "user_id" in session:
        return redirect("/dashboard")

    return render_template("login.html")



@app.route("/login", methods=["POST"])
def login():

    username = request.form["username"]
    password = request.form["password"]

    print("Username:", username)
    print("Password:", password)

    sql = """
    SELECT * FROM users
    WHERE username=%s AND password=%s
    """

    cursor.execute(sql, (username, password))

    user = cursor.fetchone()

    print("Database Result:", user)

    if user:
        session["user_id"] = user[0]
        session["username"] = user[2]
        flash("Login Successful!")
        return redirect("/dashboard")
    else:
        flash("Invalid Username or Password")
        return redirect("/")



@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        fullname = request.form["fullname"]
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        confirm = request.form["confirm_password"]

        if password != confirm:

            flash("Passwords do not match")

            return redirect("/register")

        cursor.execute(
            "SELECT * FROM users WHERE username=%s",
            (username,)
        )

        user = cursor.fetchone()

        if user:

            flash("Username already exists")

            return redirect("/register")

        sql = """
        INSERT INTO users
        (fullname, username, email, password)

        VALUES(%s,%s,%s,%s)
        """

        cursor.execute(sql,
                       (
                           fullname,
                           username,
                           email,
                           password
                       ))

        db.commit()

        flash("Registration Successful")

        return redirect("/")

    return render_template("register.html")



def login_required():

    if "user_id" not in session:

        return False

    return True



@app.route("/dashboard")
def dashboard():

    if not login_required():
        return redirect("/")

    user_id = session["user_id"]

    # Total Tasks
    cursor.execute(
        "SELECT COUNT(*) FROM tasks WHERE user_id=%s",
        (user_id,)
    )
    total_tasks = cursor.fetchone()[0]

    # Completed Tasks
    cursor.execute(
        """
        SELECT COUNT(*)
        FROM tasks
        WHERE user_id=%s
        AND status='Completed'
        """,
        (user_id,)
    )
    completed_tasks = cursor.fetchone()[0]

    # Pending Tasks
    cursor.execute(
        """
        SELECT COUNT(*)
        FROM tasks
        WHERE user_id=%s
        AND status='Pending'
        """,
        (user_id,)
    )
    pending_tasks = cursor.fetchone()[0]

    # High Priority
    cursor.execute(
        """
        SELECT COUNT(*)
        FROM tasks
        WHERE user_id=%s
        AND priority='High'
        """,
        (user_id,)
    )
    high_priority = cursor.fetchone()[0]

    # All Tasks
    cursor.execute(
        """
        SELECT
            id,
            title,
            description,
            priority,
            status,
            due_date
        FROM tasks
        WHERE user_id=%s
        ORDER BY due_date ASC
        """,
        (user_id,)
    )

    tasks = cursor.fetchall()

    return render_template(
        "dashboard.html",
        username=session["username"],
        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        pending_tasks=pending_tasks,
        high_priority=high_priority,
        tasks=tasks
    )



@app.route("/add", methods=["GET", "POST"])
def add_task():

    if not login_required():
        return redirect("/")

    if request.method == "POST":

        title = request.form["title"]
        description = request.form["description"]
        priority = request.form["priority"]
        status = request.form["status"]
        due_date = request.form["due_date"]

        sql = """
        INSERT INTO tasks
        (
            title,
            description,
            priority,
            status,
            due_date,
            user_id
        )

        VALUES
        (
            %s,
            %s,
            %s,
            %s,
            %s,
            %s
        )
        """

        cursor.execute(
            sql,
            (
                title,
                description,
                priority,
                status,
                due_date,
                session["user_id"]
            )
        )

        db.commit()

        flash("Task Added Successfully!")

        return redirect("/dashboard")

    return render_template("add_task.html")



@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_task(id):

    if not login_required():
        return redirect("/")

    if request.method == "POST":

        title = request.form["title"]
        description = request.form["description"]
        priority = request.form["priority"]
        status = request.form["status"]
        due_date = request.form["due_date"]

        sql = """
        UPDATE tasks

        SET
            title=%s,
            description=%s,
            priority=%s,
            status=%s,
            due_date=%s

        WHERE
            id=%s
        """

        cursor.execute(
            sql,
            (
                title,
                description,
                priority,
                status,
                due_date,
                id
            )
        )

        db.commit()

        flash("Task Updated Successfully!")

        return redirect("/dashboard")

    cursor.execute(
        """
        SELECT
            id,
            title,
            description,
            priority,
            status,
            due_date
        FROM tasks
        WHERE id=%s
        """,
        (id,)
    )

    task = cursor.fetchone()

    return render_template(
        "edit_task.html",
        task=task
    )
    


@app.route("/delete/<int:id>")
def delete_task(id):

    if not login_required():
        return redirect("/")

    cursor.execute(
        "DELETE FROM tasks WHERE id=%s AND user_id=%s",
        (id, session["user_id"])
    )

    db.commit()

    flash("Task Deleted Successfully!")

    return redirect("/dashboard")



@app.route("/complete/<int:id>")
def complete_task(id):

    if not login_required():
        return redirect("/")

    cursor.execute(
        """
        UPDATE tasks
        SET status='Completed'
        WHERE id=%s AND user_id=%s
        """,
        (id, session["user_id"])
    )

    db.commit()

    flash("Task Marked as Completed!")

    return redirect("/dashboard")


@app.route("/logout")
def logout():

    session.clear()

    flash("Logged Out Successfully!")

    return redirect("/")


@app.errorhandler(404)
def page_not_found(error):
    return "<h2>404 - Page Not Found</h2>", 404


@app.errorhandler(500)
def internal_error(error):
    return "<h2>500 - Internal Server Error</h2>", 500


if __name__ == "__main__":
    app.run(debug=True)