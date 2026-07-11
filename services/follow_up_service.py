from utils.db_helper import execute_query

def add_follow_up(data):
    query = """
        INSERT INTO follow_ups (application_id, follow_up_date, reminder_time, notes)
        VALUES (?, ?, ?, ?)
    """
    args = (
        data['application_id'], data['follow_up_date'], 
        data.get('reminder_time', ''), data.get('notes', '')
    )
    return execute_query(query, args, commit=True)

def get_dashboard_follow_ups(today_str):
    """Fetches follow-ups that are due today or OVERDUE, and not yet completed."""
    query = """
        SELECT f.id, f.follow_up_date, f.notes, j.company, j.role 
        FROM follow_ups f
        JOIN job_applications j ON f.application_id = j.id
        WHERE f.is_completed = 0 AND f.follow_up_date <= ?
        ORDER BY f.follow_up_date ASC
    """
    return execute_query(query, (today_str,))

def mark_follow_up_complete(follow_up_id):
    query = "UPDATE follow_ups SET is_completed = 1 WHERE id = ?"
    return execute_query(query, (follow_up_id,), commit=True)