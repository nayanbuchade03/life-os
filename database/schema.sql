CREATE TABLE IF NOT EXISTS settings (
    id INTEGER PRIMARY KEY CHECK (id = 1),
    theme TEXT DEFAULT 'dark',
    notifications_enabled INTEGER DEFAULT 1,
    last_backup_date TEXT
);

INSERT OR IGNORE INTO settings (id, theme, notifications_enabled) VALUES (1, 'dark', 1);

CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    category TEXT,
    priority TEXT CHECK(priority IN ('Low', 'Medium', 'High', 'Critical')),
    frequency TEXT CHECK(frequency IN ('Daily', 'Weekly', 'Monthly', 'Quarterly', 'One-Time', 'Custom')),
    start_date TEXT NOT NULL,
    end_date TEXT,
    reminder_time TEXT,
    estimated_time INTEGER,
    is_active INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS task_completions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task_id INTEGER NOT NULL,
    completion_date TEXT NOT NULL,
    status TEXT CHECK(status IN ('Pending', 'Completed', 'Skipped', 'Missed')) DEFAULT 'Completed',
    notes TEXT,
    FOREIGN KEY(task_id) REFERENCES tasks(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS quarterly_goals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    quarter TEXT NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    target_date TEXT,
    status TEXT CHECK(status IN ('Not Started', 'In Progress', 'Achieved', 'Failed')) DEFAULT 'Not Started',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS dsa_problems (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    problem_name TEXT NOT NULL,
    platform TEXT,
    difficulty TEXT CHECK(difficulty IN ('Easy', 'Medium', 'Hard')),
    topic TEXT,
    link TEXT,
    date_solved TEXT NOT NULL,
    time_taken INTEGER, -- In minutes
    mistakes TEXT,
    confidence_level INTEGER CHECK(confidence_level BETWEEN 1 AND 5),
    need_revision INTEGER DEFAULT 1
);

CREATE TABLE IF NOT EXISTS dsa_revisions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    problem_id INTEGER NOT NULL,
    revision_date TEXT NOT NULL,
    stage TEXT CHECK(stage IN ('1 Day', '3 Days', '7 Days', '14 Days', '30 Days', '60 Days', '90 Days')),
    status TEXT CHECK(status IN ('Pending', 'Completed', 'Missed')) DEFAULT 'Pending',
    FOREIGN KEY(problem_id) REFERENCES dsa_problems(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS job_applications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company TEXT NOT NULL,
    role TEXT NOT NULL,
    location TEXT,
    salary TEXT,
    source TEXT,
    job_link TEXT,
    resume_version TEXT,
    date_applied TEXT NOT NULL,
    current_status TEXT CHECK(current_status IN (
        'Wishlist', 'Preparing', 'Applied', 'OA Scheduled', 
        'OA Completed', 'Interview Scheduled', 'Interview Completed', 
        'Rejected', 'Offer', 'Accepted', 'Declined'
    )) DEFAULT 'Wishlist',
    notes TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS follow_ups (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    application_id INTEGER NOT NULL,
    follow_up_date TEXT NOT NULL,
    reminder_time TEXT,
    is_completed INTEGER DEFAULT 0,
    notes TEXT,
    FOREIGN KEY(application_id) REFERENCES job_applications(id) ON DELETE CASCADE
);