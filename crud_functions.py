import random
import sqlite3

connection_crud = sqlite3.connect('module_14.db')
cursor = connection_crud.cursor()

def initiate_db():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products(
    id INT PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    price INT NOT NULL
    )
    ''')

# for _ in range(1, 5):
#     cursor.execute('DELETE FROM Products WHERE title =?', (f'Продукт{_}',))
# for i in range(1,5):
#      cursor.execute('INSERT INTO Products(id, title, description, price) VALUES(?, ?, ?, ?)',
#                     (f'{i}', f'Продукт {i}', f'Описание {i}', f'{i * 100}',))

def get_all_products():
    cursor.execute('SELECT * FROM Products')
    users = cursor.fetchall()
    return users