from utils.db_helper import execute_query

def get_dsa_difficulty_distribution():
    """Returns count of DSA problems grouped by difficulty."""
    query = "SELECT difficulty, COUNT(*) as count FROM dsa_problems GROUP BY difficulty"
    return execute_query(query)

def get_job_pipeline_distribution():
    """Returns count of applications grouped by status."""
    query = "SELECT current_status, COUNT(*) as count FROM job_applications GROUP BY current_status"
    return execute_query(query)

def get_task_completion_last_7_days():
    """Returns completed task counts for the last 7 days."""
    query = """
        SELECT completion_date, COUNT(*) as count 
        FROM task_completions 
        WHERE status = 'Completed' 
        AND completion_date >= date('now', '-7 days')
        GROUP BY completion_date
        ORDER BY completion_date ASC
    """
    return execute_query(query)