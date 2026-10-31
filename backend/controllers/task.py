from flask_restful import Resource, request
from models import Task
from extensions import db, cache
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import User
from datetime import datetime

class TaskResource(Resource):
    @jwt_required()
    def get(self, task_id=None):
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)
        if task_id is None:
            if user.role == "admin":
                tasks = Task.query.all()
            else:
                tasks = Task.query.filter_by(assigned_to=user.id).all()

            data = []
            for task in tasks:
                data.append(task.to_json())
            return {"message": "all the tasks!", "tasks": data}, 200
        else:
            task = Task.query.get_or_404(task_id)
            if task.assigned_to != user.id and user.role != "admin":
                return {"message": "You are not authorized to access this task."}, 403
            task_data = task.to_json()
            return {"message": "task record of given task_id", "task": task_data}

    @jwt_required()
    def post(self):
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)
        if user.role != "admin":
            return {"message": "You are not authorized to create a task."}, 403
        data = request.get_json()
        title = data.get("title")
        description = data.get("description")
        assigned_to = data.get("assigned_to")

        task = Task(
            title=title,
            description=description,
            assigned_to=assigned_to,
            assigned_date=datetime.now() if assigned_to else None
        )
        db.session.add(task)
        db.session.commit()
        return {"message": "task created!"}, 201

    @jwt_required()
    def put(self, task_id):
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)
        task = Task.query.get_or_404(task_id)
        data = request.get_json()

        # employee can only update status of their own task
        if user.role != "admin":
            if task.assigned_to != user.id:
                return {"message": "You are not authorized to update this task."}, 403
            status = data.get("status")
            if status not in ["pending", "in-progress", "completed"]:
                return {"message": "invalid status"}, 400
            task.status = status
            if status == "completed":
                task.completed_date = datetime.now()
            db.session.commit()
            return {"message": "task status updated!!"}

        # admin can update everything
        title = data.get("title")
        description = data.get("description")
        assigned_to = data.get("assigned_to")
        status = data.get("status")

        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
        if assigned_to is not None:
            task.assigned_to = assigned_to
            task.assigned_date = datetime.now()
        if status is not None:
            task.status = status
            if status == "completed":
                task.completed_date = datetime.now()

        db.session.commit()
        return {"message": "task updated!!"}

    @jwt_required()
    def delete(self, task_id):
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)
        if user.role != "admin":
            return {"message": "You are not authorized to delete a task."}, 403
        task = Task.query.get_or_404(task_id)
        db.session.delete(task)
        db.session.commit()
        return {"message": "task deleted!!"}


class EmployeeResource(Resource):
    @jwt_required()
    def get(self):
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)
        if user.role != "admin":
            return {"message": "You are not authorized to view employees."}, 403

        employees = User.query.filter_by(role="employee").all()
        return {"employees": [employee.to_json() for employee in employees]}, 200
