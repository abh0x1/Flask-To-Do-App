from flask import Blueprint, request, render_template, redirect, url_for, session, flash
from app import db
from app.models import Task

# Blueprint with URL prefix
tasks_bp = Blueprint('tasks', __name__, url_prefix='/tasks')


# View all tasks
@tasks_bp.route('/')
def view_tasks():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    tasks = Task.query.filter_by(user_id=session['user_id']).all()
    return render_template('tasks.html', tasks=tasks)


# Add a new task
@tasks_bp.route('/add', methods=['POST'])
def add_task():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    title = request.form.get('title')
    if title:
        new_task = Task(title=title, status='Pending',
                        user_id=session['user_id'])
        db.session.add(new_task)
        db.session.commit()
        flash('Task added successfully', 'success')

    return redirect(url_for('tasks.view_tasks'))


# Toggle task status
@tasks_bp.route('/toggle/<int:task_id>', methods=['POST'])
def toggle_status(task_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    task = Task.query.filter_by(
        id=task_id, user_id=session['user_id']).first_or_404()
    if task.status == "Pending":
        task.status = "Working"
    elif task.status == "Working":
        task.status = "Done"
    else:
        task.status = "Pending"
    db.session.commit()
    return redirect(url_for('tasks.view_tasks'))


# Clear all tasks
@tasks_bp.route('/clear_tasks', methods=['POST'])
def clear_tasks():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    Task.query.filter_by(user_id=session['user_id']).delete()
    db.session.commit()
    flash('All tasks cleared!', 'info')
    return redirect(url_for('tasks.view_tasks'))


# Delete single task
@tasks_bp.route('/clear_task/<int:task_id>', methods=['POST'])
def clear_task(task_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    task = Task.query.filter_by(
        id=task_id, user_id=session['user_id']).first_or_404()
    db.session.delete(task)
    db.session.commit()
    flash('Task deleted!', 'warning')
    return redirect(url_for('tasks.view_tasks'))
