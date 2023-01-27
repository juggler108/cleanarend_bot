import sqlite3 as sq
from aiogram import Bot
from aiogram.types import Message


async def register_users():
    db = sq.connect('sqlitedb.db')
    cur = db.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, user_id VARCHAR(255), user_name VARCHAR(255))")


async def add_user_sqlite(user_id, user_name):
    db = sq.connect('sqlite.db')
    mycursor = db.cursor()

    myresult = mycursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id, )).fetchall()
    if not myresult:
        mycursor.execute("INSERT INTO users (user_id, user_name) VALUES (?, ?)", (user_id, user_name))
        db.commit()


async def db_start():
    global db, cur

    db = sq.connect('sqlite.db')
    cur = db.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS users ("
                "id INTEGER PRIMARY KEY, "
                "user_id VARCHAR(255), "
                "user_name VARCHAR(255))")

    cur.execute("CREATE TABLE IF NOT EXISTS profile("
                "name TEXT, "
                "photo TEXT, "
                "price TEXT, "
                "description TEXT)")
    db.commit()


async def db_create_product(data):
        cur.execute("INSERT INTO profile VALUES (?, ?, ?, ?)", data)
        db.commit()


async def delete_product(name):
    cur.execute("DELETE FROM profile WHERE name = ?", (name,))
    db.commit()


async def sql_read():
    return cur.execute('SELECT * FROM profile').fetchall()


async def sql_read_users():
    return cur.execute('SELECT * FROM users').fetchall()


async def sql_select_photo(name):
    return cur.execute('SELECT photo FROM profile WHERE name = ?', name)


def product_names_list():
    lst = cur.execute('SELECT * FROM profile').fetchall()
    return [i[0][1:] for i in lst]

