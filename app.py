from datetime import datetime
from typing import Dict, Optional

from flask import Flask, abort, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import joinedload


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(64), nullable=False, default="Contributor")

    tasks = db.relationship("Task", back_populates="assignee", cascade="all, delete")

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "name": self.name,
            "role": self.role,
        }


class Task(db.Model):
    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False, default="")
    status = db.Column(db.String(32), nullable=False, default="todo")
    priority = db.Column(db.String(32), nullable=False, default="medium")
    assignee_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)

    assignee = db.relationship("User", back_populates="tasks")

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "priority": self.priority,
            "assignee_id": self.assignee_id,
        }


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/api/users")
def list_users():
    all_users = User.query.order_by(User.id).all()
    return jsonify([user.to_dict() for user in all_users])


@app.post("/api/users")
def create_user():
    data = request.get_json(force=True, silent=True) or {}
    name = data.get("name", "").strip()
    if not name:
        abort(400, "User name is required.")

    user = User(name=name, role=data.get("role", "Contributor"))
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201


@app.get("/api/tasks")
def list_tasks():
    assignee_param = request.args.get("assignee_id", type=int)
    status_param = request.args.get("status")
    query = Task.query

    if assignee_param:
        query = query.filter(Task.assignee_id == assignee_param)
    if status_param:
        query = query.filter(Task.status == status_param)

    result = query.order_by(Task.id).all()
    return jsonify([task.to_dict() for task in result])


@app.post("/api/tasks")
def create_task():
    data = request.get_json(force=True, silent=True) or {} 
    title = data.get("title", "").strip()
    if not title:
        abort(400, "Task title is required.")

    assignee_id = data.get("assignee_id")
    if assignee_id is not None and not User.query.get(assignee_id):
        abort(404, f"User {assignee_id} does not exist.")

    task = Task(
        title=title,
        description=data.get("description", "").strip(),
        status=data.get("status", "todo"),
        assignee_id=assignee_id,
        priority=data.get("priority", "medium"),
    )
    db.session.add(task)
    db.session.commit()
    return jsonify(task.to_dict()), 201


@app.patch("/api/tasks/<int:task_id>")
def update_task(task_id: int):
    task = Task.query.get(task_id)
    if not task:
        abort(404, f"Task {task_id} not found.")

    data = request.get_json(force=True, silent=True) or {}

    if "assignee_id" in data:
        assignee_id = data["assignee_id"]
        if assignee_id is not None and not User.query.get(assignee_id):
            abort(404, f"User {assignee_id} does not exist.")
        task.assignee_id = assignee_id

    for key in ("title", "description", "status", "priority"):
        if key in data:
            setattr(task, key, data[key])

    db.session.commit()
    return jsonify(task.to_dict())


@app.delete("/api/tasks/<int:task_id>")
def delete_task(task_id: int):
    task = Task.query.get(task_id)
    if not task:
        abort(404, f"Task {task_id} not found.")

    db.session.delete(task)
    db.session.commit()
    return "", 204


@app.get("/api/tasks/by-assignee/<int:user_id>")
def tasks_by_assignee(user_id: int):
    user = User.query.get(user_id)
    if not user:
        abort(404, f"User {user_id} not found.")

    user_tasks = Task.query.filter(Task.assignee_id == user_id).order_by(Task.id).all()
    return jsonify({"assignee": user.to_dict(), "tasks": [task.to_dict() for task in user_tasks]})


@app.get("/api/dashboard")
def dashboard():
    serialized = [task.to_dict() for task in Task.query.all()]
    status_totals: Dict[str, int] = {}
    assignment_totals: Dict[str, int] = {}

    for task in serialized:
        status_totals[task["status"]] = status_totals.get(task["status"], 0) + 1
        assignee = task.get("assignee")
        key = assignee["name"] if assignee else "Unassigned"
        assignment_totals[key] = assignment_totals.get(key, 0) + 1

    payload = {
        "totals": {
            "tasks": Task.query.count(),
            "users": User.query.count(),
        },
        "by_status": status_totals,
        "by_assignee": assignment_totals,
    }
    return jsonify(payload)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

