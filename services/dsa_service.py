from utils.db_helper import execute_query
from datetime import datetime, timedelta

REVISION_STAGES = {
    '1 Day': 1,
    '3 Days': 3,
    '7 Days': 7,
    '14 Days': 14,
    '30 Days': 30,
    '60 Days': 60,
    '90 Days': 90
}

def get_all_problems():
    query = "SELECT * FROM dsa_problems ORDER BY date_solved DESC, id DESC"
    return execute_query(query)

def add_problem(data):
    query = """
        INSERT INTO dsa_problems (problem_name, platform, difficulty, topic, link, date_solved, time_taken, mistakes, confidence_level, need_revision)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    
    need_revision = 1 if data.get('need_revision') == 'on' else 0
    
    args = (
        data['problem_name'], data.get('platform', ''), data.get('difficulty', 'Medium'),
        data.get('topic', ''), data.get('link', ''), data['date_solved'],
        data.get('time_taken') or None, data.get('mistakes', ''),
        data.get('confidence_level', 3), need_revision
    )
    
    problem_id = execute_query(query, args, commit=True)
    
    if need_revision == 1:
        _generate_revision_schedule(problem_id, data['date_solved'])

def update_problem(problem_id, data):
    query = """
        UPDATE dsa_problems 
        SET problem_name=?, platform=?, difficulty=?, topic=?, link=?, date_solved=?, time_taken=?, mistakes=?, confidence_level=?
        WHERE id=?
    """
    args = (
        data['problem_name'], data.get('platform', ''), data.get('difficulty', 'Medium'),
        data.get('topic', ''), data.get('link', ''), data['date_solved'],
        data.get('time_taken') or None, data.get('mistakes', ''),
        data.get('confidence_level', 3), problem_id
    )
    execute_query(query, args, commit=True)

def delete_problem(problem_id):
    query = "DELETE FROM dsa_problems WHERE id = ?"
    execute_query(query, (problem_id,), commit=True)

def _generate_revision_schedule(problem_id, date_solved_str):
    """
    Helper function to calculate future dates and insert them into the dsa_revisions table.
    """
    try:
        base_date = datetime.strptime(date_solved_str, '%Y-%m-%d')
    except ValueError:
        return

    insert_query = """
        INSERT INTO dsa_revisions (problem_id, revision_date, stage, status) 
        VALUES (?, ?, ?, 'Pending')
    """
    
    for stage_name, days_to_add in REVISION_STAGES.items():
        revision_date = (base_date + timedelta(days=days_to_add)).strftime('%Y-%m-%d')
        execute_query(insert_query, (problem_id, revision_date, stage_name), commit=True)

def get_todays_revisions(date_str):
    query = """
        SELECT r.id, r.stage, p.problem_name, p.link
        FROM dsa_revisions r
        JOIN dsa_problems p ON r.problem_id = p.id
        WHERE r.revision_date = ? AND r.status = 'Pending'
    """
    return execute_query(query, (date_str,))

def mark_revision_complete(revision_id):
    query = "UPDATE dsa_revisions SET status = 'Completed' WHERE id = ?"
    return execute_query(query, (revision_id,), commit=True)