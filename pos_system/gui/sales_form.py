import wx
from pos_system.services.sales_service import add_item_to_sale, save_sale

class SalesForm(wx.Frame):
    def __init__(self, parent, title):
        super().__init__(parent, title=title, size=(850, 700))

        # Example: add button
        panel = wx.Panel(self)
        btn = wx.Button(panel, label="Add Item", pos=(10,10))
        btn.Bind(wx.EVT_BUTTON, self.on_add_item)

    def on_add_item(self, event):
        # Example data from GUI inputs
        item_code = "A101"
        qty = 2
        add_item_to_sale(item_code, qty)

    def on_save(self, event):
        save_sale()
