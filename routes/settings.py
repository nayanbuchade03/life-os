import os
import shutil
import csv
import io
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash, Response
from utils.db_helper import DATABASE_PATH, get_base_dir, execute_query

settings_bp = Blueprint('settings', __name__, url_prefix='/settings')

@settings_bp.route('/')
def index():
    db_size_mb = 0
    if os.path.exists(DATABASE_PATH):
        db_size_mb = round(os.path.getsize(DATABASE_PATH) / (1024 * 1024), 2)
        
    return render_template('settings.html', db_size=db_size_mb, db_path=DATABASE_PATH)

@settings_bp.route('/backup', methods=['POST'])
def backup():
    backups_dir = os.path.join(get_base_dir(), 'backups')
    if not os.path.exists(backups_dir):
        os.makedirs(backups_dir)
        
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_filename = f"life_os_backup_{timestamp}.db"
    backup_path = os.path.join(backups_dir, backup_filename)
    
    shutil.copy2(DATABASE_PATH, backup_path)
    return redirect(url_for('settings.index'))

@settings_bp.route('/restore', methods=['POST'])
def restore():
    if 'backup_file' not in request.files:
        return redirect(url_for('settings.index'))
        
    file = request.files['backup_file']
    if file.filename != '':
        file.save(DATABASE_PATH)
        
    return redirect(url_for('settings.index'))

@settings_bp.route('/export/<table_name>')
def export_csv(table_name):
    valid_tables = ['tasks', 'dsa_problems', 'job_applications']
    if table_name not in valid_tables:
        return "Invalid table", 400
        
    rows = execute_query(f"SELECT * FROM {table_name}")
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    if rows:
        writer.writerow(rows[0].keys())
        for row in rows:
            writer.writerow(row)
            
    response = Response(output.getvalue(), mimetype='text/csv')
    response.headers['Content-Disposition'] = f'attachment; filename={table_name}_export.csv'
    return response