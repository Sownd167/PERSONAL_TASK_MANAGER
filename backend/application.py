from flask import Flask, request, render_template, session, redirect, url_for,jsonify
import sqlite3
import re

import os

app = Flask(
    __name__,
    template_folder="../frontend" ,
    static_folder="../frontend/static"
)

app.secret_key = os.environ.get("SECRET_KEY", "dev_default_key")

#TO MAKE THE HOME PAGE VISIBLE WHEN WE RUN THE APP
@app.route("/")
def index():
    return render_template("index.html")

#TO MAKE THE SIGNUP PAGE VISIBLE
@app.route("/signup", methods=["GET","POST"])
def signup():
   message = ""
   if request.method == "POST":
    username = request.form.get("username")
    password = request.form.get("password")
    name = request.form.get("name")

    email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if not re.match(email_pattern, username):
        message = "Invalid email format."
        return render_template("signup.html", message=message)
    try:
        connection = sqlite3.connect("personaltaskmanager.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO users (username, password,name) VALUES (?, ?,?)", (username, password,name))
        connection.commit()
        connection.close()
    except sqlite3.IntegrityError:
        message = "THIS EMAIL IS ALREADY REGISTERED. TRY LOGGING IN."
        connection.close()
   return render_template("signup.html", message=message)

        
#TO MAKE THE LOGIN PAGE  VISIBLE
@app.route("/login",methods=["GET","POST"])
def login():
    message=""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_pattern,username):
            message = "Invalid email format."
            return render_template("login.html", message=message)

        connection = sqlite3.connect("personaltaskmanager.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()
        connection.close()
        if user:
            session['username'] = username
            message = "LOGIN SUCCESSFUL!"
        else:
            message = "INVALID USERNAME OR PASSWORD"
    return render_template("login.html", message=message)


@app.route("/profile_page",methods=['GET'])
def profile():
   username = session.get("username")
   if not username:
        return redirect(url_for("login"))

   connection = sqlite3.connect("personaltaskmanager.db")
   cursor = connection.cursor()

   cursor.execute("SELECT name FROM users WHERE username = ?", (username,))
   result = cursor.fetchone()
   connection.close()

   name = result[0] if result else "Not set"

   return render_template("profile_page.html", username=username, name=name)


@app.route("/edit_profile", methods=["GET", "POST"])
def edit_profile():
    username = session.get("username")
    if not username:
        return redirect(url_for("login"))

    connection = sqlite3.connect("personaltaskmanager.db")
    cursor = connection.cursor()

    if request.method == "POST":
        new_name = request.form.get("name")
        if new_name:
            cursor.execute("UPDATE users SET name = ? WHERE username = ?", (new_name, username))
            connection.commit()
            connection.close()
            return redirect(url_for("profile"))

    cursor.execute("SELECT name FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    connection.close()

    current_name = result[0] if result else ""

    return render_template("edit_profile.html", username=username, name=current_name)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


#TO MAKE THE HOME PAGE VISIBLE
@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/create_task",methods=["GET","POST"])
def create():
    message=""
    if request.method == "POST":
        taskname = request.form.get("taskname")
        description = request.form.get("desc")
        due = request.form.get("due")
        priority = request.form.get("priority")
        category = request.form.get("category")
        rem = request.form.get("remainder")
        username = session["username"]

        try:
            connection = sqlite3.connect("personaltaskmanager.db")
            cursor = connection.cursor()
            cursor.execute("""
                INSERT INTO task (taskname, description, due_date, priority, category, remainder, username)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (taskname, description, due, priority, category, rem, username))
            connection.commit()
            message = "TASK ADDED SUCCESSFULLY!"
        except sqlite3.IntegrityError:
            message = "ERROR.."
        finally:
            connection.close()

    return render_template("create_task.html",message=message)

@app.route("/task_list")
def list():
        username = session["username"]
        headings = ("TASK ID","TASK NAME","DESCRIPTION","DUE DATE","PRIORITY","CATEGORY","REMINDER","USERNAME")
        connection = sqlite3.connect("personaltaskmanager.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM task where username = ?",(username,))
        data = cursor.fetchall()
        connection.commit()
        connection.close()
        return render_template("task_list.html",headings=headings,data=data)

@app.route("/update_task")
def update():
    return render_template("update_task.html")

@app.route("/update_form_page/<update_type>")
def update_form_page(update_type):
    return render_template("update_form_page.html", update_type=update_type)

@app.route("/process_update", methods=["POST"])
def process_update():
    task_id = request.form["task_id"]
    update_type = request.form["update_type"]

    connection = sqlite3.connect("personaltaskmanager.db")
    cursor = connection.cursor()

    if update_type == "name":
        new_name = request.form["new_name"]
        cursor.execute("UPDATE task SET taskname = ? WHERE taskid = ?", (new_name, task_id))
    elif update_type == "desc":
        new_desc = request.form["new_desc"]
        cursor.execute("UPDATE task SET description = ? WHERE taskid = ?", (new_desc, task_id))
    elif update_type == "due":
        new_due = request.form["new_due"]
        cursor.execute("UPDATE task SET due_date = ? WHERE taskid = ?", (new_due, task_id))
    elif update_type == "priority":
        new_priority = request.form["new_priority"]
        cursor.execute("UPDATE task SET priority = ? WHERE taskid = ?", (new_priority, task_id))
    elif update_type == "category":
        new_category = request.form["new_category"]
        cursor.execute("UPDATE task SET category = ? WHERE taskid = ?", (new_category, task_id))
    elif update_type == "reminder":
        new_reminder = request.form["new_reminder"]
        cursor.execute("UPDATE task SET remainder = ? WHERE taskid = ?", (new_reminder, task_id))

    connection.commit()
   
    connection.close()
    return redirect(url_for("update"))


@app.route("/delete_task",methods=['GET'])
def delete():
        username = session["username"]
        headings = ("TASK ID","TASK NAME","DESCRIPTION","DUE DATE","PRIORITY","CATEGORY","REMINDER","USERNAME","DELETE")
        connection = sqlite3.connect("personaltaskmanager.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM task where username = ?",(username,))
        data = cursor.fetchall()
        connection.close()
        return render_template("delete_task.html",headings=headings,data=data)


@app.route("/deleted_task",methods=['POST'])
def deleted_tasks():
        task_id = request.form.get('task_id')
        connection = sqlite3.connect("personaltaskmanager.db")
        cursor = connection.cursor()
        cursor.execute("DELETE FROM task where taskid = ?",(task_id))
        connection.commit()
        cursor.execute("SELECT * FROM task")
        data = cursor.fetchall()
        connection.close()
        return jsonify(data)



