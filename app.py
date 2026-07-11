from flask import Flask, render_template
from datetime import datetime
from routes.tasks import tasks_bp
from routes.dsa import dsa_bp
from services import task_service

app = Flask(__name__)
app.config['SECRET_KEY'] = 'life_os_secret_key_development'

app.register_blueprint(tasks_bp)
app.register_blueprint(dsa_bp)

@app.route('/')
def dashboard():
    today_date = datetime.now().strftime('%Y-%m-%d')
    
    todays_tasks = task_service.get_todays_tasks(today_date)
    total_tasks = len(todays_tasks)
    completed_tasks = sum(1 for t in todays_tasks if t['completion_status'] == 'Completed')
    
    todays_revisions = dsa_service.get_todays_revisions(today_date)
    
    stats = {
        'tasks_completed': completed_tasks,
        'total_tasks': total_tasks,
        'current_streak': 0,
        'dsa_today': len(todays_revisions),
        'pending_followups': 0
    }
    
    return render_template('dashboard.html', 
                           today_date=today_date, 
                           stats=stats, 
                           tasks=todays_tasks,
                           revisions=todays_revisions)

if __name__ == '__main__':
    app.run(debug=True, port=5000)