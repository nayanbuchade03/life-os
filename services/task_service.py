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