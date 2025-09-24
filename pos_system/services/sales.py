from pos_system.database.db_connection import get_connection

def insert_sale(sale_main_data):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO sales (customer_name,date,total) VALUES (?, ?, ?)", (sale_main_data["customer_name"],sale_main_data["date"],sale_main_data["total"]))
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

def max_invoice_number():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT MAX(id) FROM sales")
    result = cur.fetchone()[0]
    conn.close()
    return result
