from flask import jsonify
from flask import Blueprint, render_template, request, redirect, url_for
from services import task_service

tasks_bp = Blueprint('tasks', __name__, url_prefix='/tasks')

@tasks_bp.route('/')
def index():
    tasks = task_service.get_active_tasks()
    return render_template('tasks.html', tasks=tasks)

@tasks_bp.route('/add', methods=['POST'])
def add():
    task_service.create_task(request.form)
    return redirect(url_for('tasks.index'))

@tasks_bp.route('/edit/<int:task_id>', methods=['POST'])
def edit(task_id):
    task_service.update_task(task_id, request.form)
    return redirect(url_for('tasks.index'))

@tasks_bp.route('/delete/<int:task_id>', methods=['POST'])
def delete(task_id):
    task_service.delete_task(task_id)
    return redirect(url_for('tasks.index'))

@tasks_bp.route('/log_status', methods=['POST'])
def log_status():
    data = request.get_json()
    task_id = data.get('task_id')
    date_str = data.get('date')
    status = data.get('status')
    
    if not all([task_id, date_str, status]):
        return jsonify({'error': 'Missing data'}), 400
        
    task_service.log_task_status(task_id, date_str, status)
    return jsonify({'success': True, 'status': status})