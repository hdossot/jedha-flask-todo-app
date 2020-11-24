from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

DATABASE = "./todo.db"

# comment
def create_app() -> Flask:
    app = Flask(__name__)
    # uncomment below to use a file rather than memory database
    # app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + DATABASE
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    db = SQLAlchemy(app)

    class Todo(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        title = db.Column(db.String(80))
        complete = db.Column(db.Boolean)

    @app.route("/")
    def index():
        todo_list = Todo.query.all()
        return render_template("index.html", todo_list=todo_list)

    @app.route("/add", methods=["POST"])
    def add():
        title = request.form.get("title")
        new_todo = Todo(title=title, complete=False)
        db.session.add(new_todo)
        db.session.commit()
        return redirect(url_for("index"))

    @app.route("/complete/<string:todo_id>")
    def complete(todo_id):
        todo = Todo.query.filter_by(id=todo_id).first()
        todo.complete = not todo.complete
        db.session.commit()
        return redirect(url_for("index"))

    @app.route("/delete/<string:todo_id>")
    def delete(todo_id):
        todo = Todo.query.filter_by(id=todo_id).first()
        db.session.delete(todo)
        db.session.commit()
        return redirect(url_for("index"))

    db.create_all()
    return app