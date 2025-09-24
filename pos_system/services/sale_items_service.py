from pos_system.database.db_connection import execute_query
from pos_system.services.sales_service import save_sale

def save_sale_items(sale_id,items):
        """
        Save multiple sale items at once.
        items = list of dicts like:
        [{"item_id": 1, "qty": 2, "price": 100.0}, ...]
        """
        sale_id = sale_id
        for item in items:
            total = item["qty"] * item["price"]
            execute_query("""
                INSERT INTO sale_items (sale_id, item_id, qty, price, total)
                VALUES (?, ?, ?, ?, ?)
            """, (sale_id, item["item_id"], item["qty"], item["price"], total))

    