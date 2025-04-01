import json
import os.path
import sqlite3


def connect(path):
    exists = os.path.exists(path)
    __conn = sqlite3.connect(path)
    if not exists:
        create_tables(__conn)
    __conn.row_factory = sqlite3.Row
    return __conn


def create_tables(conn):
    conn.execute('''
        CREATE TABLE IF NOT EXISTS carts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            contents TEXT,
            cost REAL
        )
    ''')
    conn.commit()


def get_cart(username: str) -> list:
    conn = connect('carts.db')
    cursor = conn.cursor()
    cursor.execute('SELECT contents FROM carts WHERE username = ?', (username,))
    
    cart = cursor.fetchone()
    if cart is None:
        cursor.close()
        conn.close()
        return []

    try:
        contents = json.loads(cart['contents'])
    except json.JSONDecodeError:
        cursor.close()
        conn.close()
        return []  # If data is malformed, return an empty list
    
    # If contents are valid, return them
    cursor.close()
    conn.close()
    return contents


def add_to_cart(username: str, product_id: int):
    conn = connect('carts.db')
    cursor = conn.cursor()
    cursor.execute('SELECT contents FROM carts WHERE username = ?', (username,))
    contents = cursor.fetchone()
    
    if contents is None:
        contents = []  # Start a new list if the cart doesn't exist
    else:
        try:
            contents = json.loads(contents['contents'])
        except json.JSONDecodeError:
            contents = []  # If contents are malformed, reset to an empty list
    
    contents.append(product_id)  # Add the new product to the cart

    cursor.execute('INSERT OR REPLACE INTO carts (username, contents, cost) VALUES (?, ?, ?)',
                   (username, json.dumps(contents), 0))  # Save the updated cart
    conn.commit()
    cursor.close()
    conn.close()


def remove_from_cart(username: str, product_id: int):
    conn = connect('carts.db')
    cursor = conn.cursor()
    cursor.execute('SELECT contents FROM carts WHERE username = ?', (username,))
    contents = cursor.fetchone()
    
    if contents is None:
        cursor.close()
        conn.close()
        return

    try:
        contents = json.loads(contents['contents'])
    except json.JSONDecodeError:
        cursor.close()
        conn.close()
        return  # If the data is malformed, exit without doing anything
    
    if product_id in contents:
        contents.remove(product_id)  # Remove the specified product

    cursor.execute('INSERT OR REPLACE INTO carts (username, contents, cost) VALUES (?, ?, ?)',
                   (username, json.dumps(contents), 0))  # Save the updated cart
    conn.commit()
    cursor.close()
    conn.close()


def delete_cart(username: str):
    conn = connect('carts.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM carts WHERE username = ?', (username,))
    conn.commit()
    cursor.close()
    conn.close()
