from pos_system.services.sales import insert_sale, max_invoice_number
from pos_system.utils.helpers import calculate_total
from pos_system.database.db_connection import execute_query

cart = []  # Temporary list before saving

def save_sale(sale_main_data):
    execute_query("""
        INSERT INTO sales (customer_name, date, total)
        VALUES (?, ?, ?)
    """, (sale_main_data["customer_name"], sale_main_data["date"], sale_main_data["total"]))


def generate_invoice_number():
    result = max_invoice_number()
    if result:
        new_invoice = int(result) + 1
    else:
        new_invoice = 1  # first invoice

    return new_invoice   