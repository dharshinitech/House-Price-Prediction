import sqlite3


def create_connection():

    connection = sqlite3.connect("users.db")

    return connection


def create_users_table():

    connection = create_connection()

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    connection.commit()

    connection.close()


def register_user(email, password):

    connection = create_connection()

    cursor = connection.cursor()

    try:

        cursor.execute(
            "INSERT INTO users (email, password) VALUES (?, ?)",
            (email, password)
        )

        connection.commit()

        return True

    except sqlite3.IntegrityError:

        return False

    finally:

        connection.close()


def login_user(email, password):

    connection = create_connection()

    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE email = ? AND password = ?",
        (email, password)
    )

    user = cursor.fetchone()

    connection.close()

    return user


create_users_table()