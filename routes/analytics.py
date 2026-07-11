import json
from flask import Blueprint, render_template
from services import analytics_service
from datetime import datetime, timedelta

analytics_bp = Blueprint('analytics', __name__, url_prefix='/analytics')

@analytics_bp.route('/')
def index():
    dsa_raw = analytics_service.get_dsa_difficulty_distribution()
    dsa_labels = [row['difficulty'] for row in dsa_raw]
    dsa_data = [row['count'] for row in dsa_raw]

    jobs_raw = analytics_service.get_job_pipeline_distribution()
    jobs_labels = [row['current_status'] for row in jobs_raw]
    jobs_data = [row['count'] for row in jobs_raw]

    tasks_raw = analytics_service.get_task_completion_last_7_days()
    tasks_dict = {row['completion_date']: row['count'] for row in tasks_raw}
    
    tasks_labels = []
    tasks_data = []
    today = datetime.now()
    
    for i in range(6, -1, -1):
        day_str = (today - timedelta(days=i)).strftime('%Y-%m-%d')
        tasks_labels.append(day_str)
        tasks_data.append(tasks_dict.get(day_str, 0))

    return render_template(
        'analytics.html',
        dsa_labels=json.dumps(dsa_labels), dsa_data=json.dumps(dsa_data),
        jobs_labels=json.dumps(jobs_labels), jobs_data=json.dumps(jobs_data),
        tasks_labels=json.dumps(tasks_labels), tasks_data=json.dumps(tasks_data)
    )