import sqlite3

def get_connection():
    return sqlite3.connect('database.db')

def init_db():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_stats (
        user_id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        total_solved INTEGER DEFAULT 0,
        solved_correctly INTEGER DEFAULT 0
    )
    ''')
    connection.commit()
    connection.close()

def create_user(user_id, username):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            'INSERT OR IGNORE INTO user_stats (user_id, username) VALUES (?, ?)',
            (user_id, username,)
        )
        connection.commit()
        connection.close()
        print(f'Пользователь {username} создан или найден успешно.')
    except Exception as e:
        print(f'Ошибка при создании пользователя {username}: {e}')


def get_user_stats(user_id, username):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            'SELECT total_solved, solved_correctly FROM user_stats WHERE user_id = ?',
            (user_id,)
        )
        result = cursor.fetchone()
        connection.close()
        if result:
            return {'total_solved': result[0], 'solved_correctly': result[1]}
        else:
            create_user(user_id, username)
            return {'total_solved': 0, 'solved_correctly': 0}
    except Exception as e:
        print(f'Ошибка при получении статистики у {username}: {e}')
        return {'total_solved': 0, 'solved_correctly': 0}


def update_stats(user_id, is_correct, username):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute('''
            UPDATE user_stats 
            SET total_solved = total_solved + 1
            WHERE user_id = ?
        ''', (user_id,))
        if is_correct:
            cursor.execute('''
                UPDATE user_stats 
                SET solved_correctly = solved_correctly + 1
                WHERE user_id = ?
            ''', (user_id,))
        connection.commit()
        connection.close()
        print(f'Статистика пользователя {username} обновлена')

    except Exception as e:
        print(f'Ошибка при обновлении статистики у {username}: {e}')
        create_user(user_id, username)
        update_stats(user_id, is_correct, username)

# Инициализация базы данных при импорте
init_db()