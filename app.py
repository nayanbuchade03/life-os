from flask import Flask, render_template
from datetime import datetime
from routes.tasks import tasks_bp

app = Flask(__name__)
app.config['SECRET_KEY'] = 'life_os_secret_key_development'

app.register_blueprint(tasks_bp)

@app.route('/')
def dashboard():
    today_date = datetime.now().strftime('%Y-%m-%d')
    stats = {
        'tasks_completed': 0, 'total_tasks': 0,
        'current_streak': 0, 'dsa_today': 0, 'pending_followups': 0
    }
    return render_template('dashboard.html', today_date=today_date, stats=stats)

if __name__ == '__main__':
    app.run(debug=True, port=5000)