import base64
import secrets
import sqlite3 as sql

_conn = sql.connect(":memory:", check_same_thread=False)


def init_db():
    c = _conn.cursor()

    with open("init.sql") as f:
        c.executescript(f.read())

    # users = [
    #     ("admin", secrets.token_hex(32)),
    # ]

    # c.executemany(
    #     "INSERT INTO users (username, password) VALUES (?, ?)",
    #     users
    # )

    result = c.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        ("admin", secrets.token_hex(32)),
    )

    admin_id = result.lastrowid

    with open("flag.txt") as f:
        flag_content = f.read().strip()

    encoded_flag = base64.b64encode(flag_content.encode()).decode()

    notes = [
        ("Debug test", "This is a test note for debugging purposes.", 1),
        ("Hello World", "Hello, World!", 1),
        (
            "Secret Recipe",
            "The secret recipe is 1 cup of sugar, 2 cups of flour, and 3 cups of love.",
            1,
        ),
        ("Welcome Note", "Welcome to the Secret Note Manager!", 0),
        ("Confidential Flag", encoded_flag, 1),
    ]

    c.executemany(
        "INSERT INTO notes (user_id, title, content, is_private) VALUES (?, ?, ?, ?)",
        [(admin_id, *note) for note in notes],
    )

    _conn.commit()


def login_user(username, password):
    c = _conn.cursor()
    c.execute(
        f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    )
    return c.fetchone()


def get_user_by_id(user_id):
    c = _conn.cursor()
    c.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return c.fetchone()


class Note:
    def __init__(self, id, user_id, title, content, is_private):
        self.id = id
        self.user_id = user_id
        self.title = title
        self.content = content
        self.is_private = is_private

    @property
    def username(self):
        user = get_user_by_id(self.user_id)
        return user[1]


def get_all_public_notes():
    c = _conn.cursor()
    c.execute("SELECT * FROM notes WHERE is_private = 0")
    notes = c.fetchall()
    return [Note(*note) for note in notes]


def get_user_notes(user_id):
    c = _conn.cursor()
    c.execute("SELECT * FROM notes WHERE user_id = ?", (user_id,))
    notes = c.fetchall()
    return [Note(*note) for note in notes]
