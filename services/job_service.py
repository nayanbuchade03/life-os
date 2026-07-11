from utils.db_helper import execute_query

def get_all_applications():
    query = "SELECT * FROM job_applications ORDER BY date_applied DESC, id DESC"
    return execute_query(query)

def get_pipeline_stats():
    """Calculates counts for the pipeline overview."""
    query = """
        SELECT 
            SUM(CASE WHEN current_status IN ('Applied', 'Wishlist', 'Preparing') THEN 1 ELSE 0 END) as active_applications,
            SUM(CASE WHEN current_status IN ('OA Scheduled', 'OA Completed', 'Interview Scheduled', 'Interview Completed') THEN 1 ELSE 0 END) as interviewing,
            SUM(CASE WHEN current_status IN ('Offer', 'Accepted') THEN 1 ELSE 0 END) as offers,
            SUM(CASE WHEN current_status IN ('Rejected', 'Declined') THEN 1 ELSE 0 END) as closed
        FROM job_applications
    """
    return execute_query(query, fetchone=True)

def add_application(data):
    query = """
        INSERT INTO job_applications (company, role, location, salary, source, job_link, resume_version, date_applied, current_status, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    args = (
        data['company'], data['role'], data.get('location', ''), data.get('salary', ''),
        data.get('source', ''), data.get('job_link', ''), data.get('resume_version', ''),
        data['date_applied'], data.get('current_status', 'Applied'), data.get('notes', '')
    )
    return execute_query(query, args, commit=True)

def update_application(app_id, data):
    query = """
        UPDATE job_applications 
        SET company=?, role=?, location=?, salary=?, source=?, job_link=?, resume_version=?, date_applied=?, current_status=?, notes=?, updated_at=CURRENT_TIMESTAMP
        WHERE id=?
    """
    args = (
        data['company'], data['role'], data.get('location', ''), data.get('salary', ''),
        data.get('source', ''), data.get('job_link', ''), data.get('resume_version', ''),
        data['date_applied'], data.get('current_status', 'Applied'), data.get('notes', ''),
        app_id
    )
    execute_query(query, args, commit=True)

def delete_application(app_id):
    query = "DELETE FROM job_applications WHERE id = ?"
    execute_query(query, (app_id,), commit=True)