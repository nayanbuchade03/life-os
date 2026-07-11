from utils.db_helper import execute_query

def get_active_tasks():
    query = "SELECT * FROM tasks WHERE is_active = 1 ORDER BY start_date DESC"
    return execute_query(query)

def create_task(data):
    query = """
        INSERT INTO tasks (title, description, category, priority, frequency, start_date, end_date, reminder_time, estimated_time)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    args = (
        data['title'], data.get('description', ''), data.get('category', 'General'), 
        data['priority'], data['frequency'], data['start_date'], 
        data.get('end_date'), data.get('reminder_time'), data.get('estimated_time')
    )
    return execute_query(query, args, commit=True)

def update_task(task_id, data):
    query = """
        UPDATE tasks 
        SET title=?, description=?, category=?, priority=?, frequency=?, start_date=?, end_date=?, reminder_time=?, estimated_time=?
        WHERE id=?
    """
    args = (
        data['title'], data.get('description', ''), data.get('category', 'General'), 
        data['priority'], data['frequency'], data['start_date'], 
        data.get('end_date'), data.get('reminder_time'), data.get('estimated_time'),
        task_id
    )
    return execute_query(query, args, commit=True)

def delete_task(task_id):
    query = "UPDATE tasks SET is_active = 0 WHERE id = ?"
    return execute_query(query, (task_id,), commit=True)


def get_todays_tasks(date_str):
    """
    Fetches Daily tasks and any tasks scheduled for or before today.
    Joins with task_completions to get the current status for today.
    """
    query = """
        SELECT t.id, t.title, t.priority, t.category, 
               COALESCE(tc.status, 'Pending') as completion_status
        FROM tasks t
        LEFT JOIN task_completions tc 
               ON t.id = tc.task_id AND tc.completion_date = ?
        WHERE t.is_active = 1 
          AND (t.frequency = 'Daily' OR t.start_date <= ?)
        ORDER BY 
          -- Order by completion status first (pending at top), then priority
          COALESCE(tc.status, 'Pending') DESC,
          CASE t.priority 
              WHEN 'Critical' THEN 1 
              WHEN 'High' THEN 2 
              WHEN 'Medium' THEN 3 
              ELSE 4 
          END
    """
    return execute_query(query, (date_str, date_str))

def log_task_status(task_id, date_str, status):
    """
    Inserts or updates the daily log for a specific task.
    """
    # Check if a log already exists for this task on this date
    check_query = "SELECT id FROM task_completions WHERE task_id = ? AND completion_date = ?"
    existing = execute_query(check_query, (task_id, date_str), fetchone=True)
    
    if existing:
        update_query = "UPDATE task_completions SET status = ? WHERE id = ?"
        return execute_query(update_query, (status, existing['id']), commit=True)
    else:
        insert_query = "INSERT INTO task_completions (task_id, completion_date, status) VALUES (?, ?, ?)"
        return execute_query(insert_query, (task_id, date_str, status), commit=True)