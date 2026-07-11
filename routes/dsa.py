from flask import Blueprint, render_template, request, redirect, url_for
from services import dsa_service
from datetime import datetime

dsa_bp = Blueprint('dsa', __name__, url_prefix='/dsa')

@dsa_bp.route('/')
def index():
    problems = dsa_service.get_all_problems()
    today_date = datetime.now().strftime('%Y-%m-%d')
    return render_template('dsa.html', problems=problems, today_date=today_date)

@dsa_bp.route('/add', methods=['POST'])
def add():
    dsa_service.add_problem(request.form)
    return redirect(url_for('dsa.index'))

@dsa_bp.route('/edit/<int:problem_id>', methods=['POST'])
def edit(problem_id):
    dsa_service.update_problem(problem_id, request.form)
    return redirect(url_for('dsa.index'))

@dsa_bp.route('/delete/<int:problem_id>', methods=['POST'])
def delete(problem_id):
    dsa_service.delete_problem(problem_id)
    return redirect(url_for('dsa.index'))