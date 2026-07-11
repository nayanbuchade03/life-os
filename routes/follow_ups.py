from flask import Blueprint, request, redirect, url_for, jsonify
from services import follow_up_service

follow_ups_bp = Blueprint('follow_ups', __name__, url_prefix='/follow_ups')

@follow_ups_bp.route('/add', methods=['POST'])
def add():
    follow_up_service.add_follow_up(request.form)
    return redirect(url_for('jobs.index'))

@follow_ups_bp.route('/toggle', methods=['POST'])
def toggle():
    data = request.get_json()
    follow_up_id = data.get('follow_up_id')
    
    if follow_up_id:
        follow_up_service.mark_follow_up_complete(follow_up_id)
        return jsonify({'success': True})
        
    return jsonify({'error': 'Invalid ID'}), 400