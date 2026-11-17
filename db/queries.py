
CREATE_USERS_TABLE = '''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id INTEGER NOT NULL UNIQUE,
        username TEXT
    )
'''


CREATE_TASKS_TABLE = '''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        is_done BOOLEAN NOT NULL DEFAULT 0,

        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    )
'''

GET_USER_BY_TG_ID = 'SELECT * FROM users WHERE telegram_id = ?'

INSERT_USER = 'INSERT OR IGNORE INTO users (telegram_id, username) VALUES (?, ?)'



GET_TASK_BY_ID = 'SELECT * FROM tasks WHERE id = ?'

INSERT_TASK = 'INSERT INTO tasks (user_id, title) VALUES (?, ?)'

UPDATE_TASK_DONE = 'UPDATE tasks SET is_done = 1 WHERE id = ?'

GET_USER_TASKS = '''
    SELECT t.id, t.title, t.is_done
    FROM tasks AS t
    INNER JOIN users AS u
        ON u.id = t.user_id
    WHERE u.telegram_id = ?
    ORDER BY t.id
'''


GET_STATS = '''
    SELECT COUNT(*) AS total,
           SUM(is_done) AS done
    FROM tasks
    WHERE user_id = ?
    GROUP BY user_id
'''
