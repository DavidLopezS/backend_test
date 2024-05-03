import sqlite3

def get_connection(db_path: str):
    return sqlite3.connect(db_path)

def create_user_profiles_table(db_path: str):
    conn = get_connection(db_path)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS user_profiles (
                        id TEXT PRIMARY KEY,
                        email TEXT,
                        linkedin_url TEXT,
                        current_job_title TEXT,
                        current_job_subtitle TEXT,
                        current_job_caption TEXT,
                        current_job_metadata TEXT
                    )''')
    conn.commit()
    conn.close()
