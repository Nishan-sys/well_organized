from ..database.db_connection import get_connection

def get_all_products():
    """Fetch all products from final_item table."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM final_item")
    products = cursor.fetchall()
    conn.close()
    return products