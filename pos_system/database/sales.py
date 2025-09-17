from pos_system.database.db_connection import get_connection

def insert_sale():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO sales (date) VALUES (datetime('now'))")
    sale_id = cur.lastrowid
    conn.commit()
    conn.close()
    return sale_id

def insert_sale_item(sale_id, item_code, qty, price, total):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO sale_items (sale_id, item_code, qty, price, total) VALUES (?, ?, ?, ?, ?)",
        (sale_id, item_code, qty, price, total),
    )
    conn.commit()
    conn.close()
