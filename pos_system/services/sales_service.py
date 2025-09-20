from pos_system.database.sales import insert_sale, max_invoice_number
from pos_system.utils.helpers import calculate_total

cart = []  # Temporary list before saving

def add_item_to_sale(item_code, qty):
    # (Fake product info for now)
    price = 100  
    total = calculate_total(qty, price)
    cart.append((item_code, qty, price, total))
    print(f"Item added: {item_code}, Qty: {qty}, Total: {total}")

def save_sale(sale_main_data):
    sale_id = insert_sale(sale_main_data)
    print(f"New sale created with ID: {sale_id}")
    '''
    for item in cart:
        item_code, qty, price, total = item
        insert_sale_item(sale_id, item_code, qty, price, total)
    print("Sale saved!")
'''
def generate_invoice_number():
    result = max_invoice_number()
    if result:
        new_invoice = int(result) + 1
    else:
        new_invoice = 1  # first invoice

    return new_invoice   