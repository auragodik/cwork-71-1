from db.database import get_db
from db.queries import (
    GET_TASK_BY_ID, INSERT_TASK, UPDATE_TASK_DONE,
    GET_USER_TASKS, GET_STATS
)


def add_task(user_id: int, title: str):
    conn = get_db()
    conn.execute(INSERT_TASK, (user_id, title))
    conn.commit()
    conn.close()


def get_tasks(telegram_id: int):
    conn = get_db()
    tasks = conn.execute(GET_USER_TASKS, (telegram_id, )).fetchall()
    conn.close()
    return [dict(task) for task in tasks]


def task_done(task_id: int, user_id: int):

    conn = get_db()
    task = conn.execute(GET_TASK_BY_ID, (task_id, )).fetchone()

    if not task or task['user_id'] != user_id:
        conn.close()
        return False

    conn.execute(UPDATE_TASK_DONE, (task_id, ))
    conn.commit()
    conn.close()
    return True


def get_stats(user_id: int):
    conn = get_db()
    row = conn.execute(GET_STATS, (user_id, )).fetchone()
    conn.close()

    if not row:
        return {'total': 0, 'done': 0, 'not_done': 0}

    return {
        'total': row['total'],
        'done': row['done'],
        'not_done': row['total'] - row['done']
    }