from app import celery
from models import User
from extensions import mail
from flask_mail import Message


@celery.task(name="tasks.background_task")
def background_task():
    return "Background task completed"


@celery.task(name="tasks.daily_reminder")
def daily_reminder():
    employees = User.query.filter_by(role='employee').all()
    for employee in employees:
        tasks = employee.tasks
        tasks_list = ""
        for task in tasks:
            tasks_list += f"{task.title} - {task.status}\n"

        msg = Message(
            subject="daily task reminder",
            recipients=[employee.email],
            body=f"Hii {employee.full_name}, reminder to check your open tasks: {tasks_list}",
        )
        mail.send(msg)

    return {"message": "Daily reminder sent to all employees"}
