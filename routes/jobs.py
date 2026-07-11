from flask import Blueprint, render_template, request, redirect, url_for
from services import job_service
from datetime import datetime

jobs_bp = Blueprint('jobs', __name__, url_prefix='/jobs')

@jobs_bp.route('/')
def index():
    applications = job_service.get_all_applications()
    stats = job_service.get_pipeline_stats()
    today_date = datetime.now().strftime('%Y-%m-%d')
    return render_template('jobs.html', applications=applications, stats=stats, today_date=today_date)

@jobs_bp.route('/add', methods=['POST'])
def add():
    job_service.add_application(request.form)
    return redirect(url_for('jobs.index'))

@jobs_bp.route('/edit/<int:app_id>', methods=['POST'])
def edit(app_id):
    job_service.update_application(app_id, request.form)
    return redirect(url_for('jobs.index'))

@jobs_bp.route('/delete/<int:app_id>', methods=['POST'])
def delete(app_id):
    job_service.delete_application(app_id)
    return redirect(url_for('jobs.index'))