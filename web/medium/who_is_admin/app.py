import sqlite3

conn = sqlite3.connect("app.db")
cursor = conn.cursor()


def setup_db():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password TEXT NOT NULL
    )
    """)
    cursor.execute("""
    INSERT INTO users (username, password) VALUES
    ('admin', 'admin123'),
    ('john', 'password1'),
    ('john', 'password2')
    """)

    conn.commit()


def login(username, password):
    query = (
        f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    )
    cursor.execute(query)

    user = cursor.fetchone()
    if user:
        print(f"Welcome, {username}!")
    else:
        print("Invalid username or password")


if __name__ == "__main__":
    setup_db()
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    login(username, password)
    conn.close()
