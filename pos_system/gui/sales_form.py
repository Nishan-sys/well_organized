import wx
from ..services.sales_service import save_sale, generate_invoice_number
from ..services.product_service import get_all_products
from ..services.sale_items_service import save_sale_items
import wx.adv 
from datetime import datetime
class SalesForm(wx.Frame):
    def __init__(self, parent, title):
        super().__init__(parent, title=title, size=(850, 700))
        
        self.products = get_all_products()  # Load products from DB
        self.item_id_hidden = None
        # Example: add button
        self.panel = wx.Panel(self)
        self.panel.SetBackgroundColour('#f0f4f7')

        main_sizer = wx.BoxSizer(wx.VERTICAL)

        # Title
        title_text = wx.StaticText(self.panel, label="SLTC - BILLING SYSTEM")
        title_font = wx.Font(18, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        title_text.SetFont(title_font)
        title_text.SetForegroundColour('#2d6cdf')
        main_sizer.Add(title_text, 0, wx.ALIGN_CENTER | wx.TOP, 20)

        # Customer Info
        # --- Customer Info Section ---
        cust_box = wx.StaticBox(self.panel, label="Customer Info")
        cust_box.SetForegroundColour('#1e8449')
        cust_sizer = wx.StaticBoxSizer(cust_box, wx.HORIZONTAL)

        # Use FlexGridSizer with 1 row and 6 columns (Label + Field for each)
        cust_grid = wx.FlexGridSizer(1, 6, 10, 10)

        # --- Invoice Number ---
        cust_grid.Add(wx.StaticText(self.panel, label="Invoice No:"), 0, wx.ALIGN_CENTER_VERTICAL)
        self.invoice_no = wx.TextCtrl(self.panel, style=wx.TE_READONLY)  # read-only so user can't edit
        self.new_invoice_id = generate_invoice_number()
        self.invoice_no.SetValue(f"INV{self.new_invoice_id:05d}")  # Placeholder text
        cust_grid.Add(self.invoice_no, 1, wx.EXPAND)

        # --- Customer Name ---
        cust_grid.Add(wx.StaticText(self.panel, label="Customer Name:"), 0, wx.ALIGN_CENTER_VERTICAL)
        self.cust_name = wx.TextCtrl(self.panel)
        cust_grid.Add(self.cust_name, 1, wx.EXPAND)

        # --- Date ---
        cust_grid.Add(wx.StaticText(self.panel, label="Date:"), 0, wx.ALIGN_CENTER_VERTICAL)
        self.date_picker = wx.adv.DatePickerCtrl(self.panel)
        cust_grid.Add(self.date_picker, 1, wx.EXPAND)

        # Add grid to box
        cust_sizer.Add(cust_grid, 1, wx.ALL | wx.EXPAND, 10)

        # Add box to main layout
        main_sizer.Add(cust_sizer, 0, wx.ALL | wx.EXPAND, 15)

       
        # Item Entry
        item_box = wx.StaticBox(self.panel, label="Add Item")
        item_box.SetForegroundColour('#b9770e')
        item_sizer = wx.StaticBoxSizer(item_box, wx.HORIZONTAL)
        item_grid = wx.FlexGridSizer(1, 8, 10, 10)
        item_grid.Add(wx.StaticText(self.panel, label="Item Code/Name:"), 0, wx.ALIGN_CENTER_VERTICAL)
        self.item_code = wx.TextCtrl(self.panel)
        item_grid.Add(self.item_code, 1, wx.EXPAND)
        
        item_grid.Add(wx.StaticText(self.panel, label="Description:"), 0, wx.ALIGN_CENTER_VERTICAL)
        self.item_desc = wx.TextCtrl(self.panel)
        item_grid.Add(self.item_desc, 1, wx.EXPAND)
        item_grid.Add(wx.StaticText(self.panel, label="Price:"), 0, wx.ALIGN_CENTER_VERTICAL)
        self.item_price = wx.TextCtrl(self.panel)    
        item_grid.Add(self.item_price, 1, wx.EXPAND)
        item_grid.Add(wx.StaticText(self.panel, label="Qty:"), 0, wx.ALIGN_CENTER_VERTICAL)
        self.item_qty = wx.SpinCtrl(self.panel, min=1, max=1000, initial=1)
        item_grid.Add(self.item_qty, 1, wx.EXPAND)
        item_sizer.Add(item_grid, 1, wx.ALL | wx.EXPAND, 10)
        self.add_btn = wx.Button(self.panel, label="Add", size=(70, 30))
        self.add_btn.SetBackgroundColour('#2ecc71')
        self.add_btn.SetForegroundColour('white')
        item_sizer.Add(self.add_btn, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 10)
        main_sizer.Add(item_sizer, 0, wx.ALL | wx.EXPAND, 10)


        # Item Search Results
        search_box = wx.StaticBox(self.panel, label="Search Results")
        search_box.SetForegroundColour('#8e44ad')   # purple for distinction
        search_sizer = wx.StaticBoxSizer(search_box, wx.VERTICAL)

        self.search_list = wx.ListCtrl(self.panel, style=wx.LC_REPORT | wx.BORDER_SUNKEN)
        self.search_list.InsertColumn(0, "Item Code/Name", width=150)
        self.search_list.InsertColumn(1, "Description", width=250)
        self.search_list.InsertColumn(2, "Cost", width=100)
        self.search_list.InsertColumn(3, "Price", wx.LIST_FORMAT_RIGHT, 100)

        search_sizer.Add(self.search_list, 1, wx.ALL | wx.EXPAND, 5)
        self.search_list.SetMinSize(( -1, 60 ))
        main_sizer.Add(search_sizer, 1, wx.ALL | wx.EXPAND, 10)
        


        # Sales List
        list_box = wx.StaticBox(self.panel, label="Sales Items")
        list_box.SetForegroundColour('#2874a6')
        list_sizer = wx.StaticBoxSizer(list_box, wx.VERTICAL)
        self.sales_list = wx.ListCtrl(self.panel, style=wx.LC_REPORT | wx.BORDER_SUNKEN)
        self.sales_list.InsertColumn(0, "Item Code/Name", width=150)
        self.sales_list.InsertColumn(1, "Description", width=250)
        self.sales_list.InsertColumn(2, "Qty", wx.LIST_FORMAT_CENTER, 60)
        self.sales_list.InsertColumn(3, "Price", wx.LIST_FORMAT_RIGHT, 100)
        self.sales_list.InsertColumn(4, "Total", wx.LIST_FORMAT_RIGHT, 100)
        list_sizer.Add(self.sales_list, 1, wx.ALL | wx.EXPAND, 5)
        main_sizer.Add(list_sizer, 1, wx.ALL | wx.EXPAND, 10)

       

        # Total and Buttons
        bottom_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.total_label = wx.StaticText(self.panel, label="Total: Rs:0.00")
        total_font = wx.Font(14, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        self.total_label.SetFont(total_font)
        self.total_label.SetForegroundColour('#c0392b')
        bottom_sizer.Add(self.total_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 10)
        bottom_sizer.AddStretchSpacer()
        self.save_btn = wx.Button(self.panel, label="Save Sale", size=(100, 35))
        self.save_btn.SetBackgroundColour('#2980b9')
        self.save_btn.SetForegroundColour('white')
        bottom_sizer.Add(self.save_btn, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 10)
        self.clear_btn = wx.Button(self.panel, label="Clear", size=(80, 35))
        self.clear_btn.SetBackgroundColour('#f39c12')
        self.clear_btn.SetForegroundColour('white')
        bottom_sizer.Add(self.clear_btn, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 10)
        main_sizer.Add(bottom_sizer, 0, wx.EXPAND | wx.ALL, 10)

        self.panel.SetSizer(main_sizer)

        # Bind events
        self.search_list.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.on_search_item_click) 
        self.item_code.Bind(wx.EVT_TEXT, self.on_search)
        self.item_code.Bind(wx.EVT_KILL_FOCUS, self.on_leave)
        self.add_btn.Bind(wx.EVT_BUTTON, self.on_add_item)
        self.save_btn.Bind(wx.EVT_BUTTON, self.on_save_sale)
        self.clear_btn.Bind(wx.EVT_BUTTON, self.on_clear)
        self.populate_product_list()
        self.Centre()
        self.Show()

   
    def on_save(self, event):
        save_sale()

    def on_leave(self, event):
        if self.item_code.GetValue():
            if self.search_list.GetItemCount() > 0:
                item_name = self.search_list.GetItemText(0,0)
                item_desc = self.search_list.GetItemText(0,1)
                item_price = self.search_list.GetItemText(0,3).replace("Rs:","")
                self.item_code.SetValue(item_name)
                self.item_desc.SetValue(item_desc)
                self.item_price.SetValue(item_price)
                self.item_price.SetFocus()
            event.Skip()

    def populate_product_list(self, filter_text=""):
        """Populate the product list, optionally filtering by search text."""
        self.search_list.DeleteAllItems()
        filter_lower = filter_text.lower()
        
        for item in self.products:
            if filter_lower in item[2].lower():
                index = self.search_list.InsertItem(self.search_list.GetItemCount(), item[2])
                self.search_list.SetItem(index, 1, item[3])
                self.search_list.SetItem(index, 2, f"Rs:{item[4]}")
                self.search_list.SetItem(index, 3, f"Rs:{item[5]}")
                self.search_list.SetItemData(index, item[0])
        self.search_list.Select(0)  # Select the first item by default
        self.search_list.Focus(0)

    def on_search(self, event):
        search_term = self.item_code.GetValue()
        self.item_desc.SetValue("")
        self.item_price.SetValue("")
        self.populate_product_list(search_term)
        #testing comment

    def on_search_item_click(self, event):
        index = event.GetIndex()
        item_name = self.search_list.GetItemText(index, 0)
        item_desc = self.search_list.GetItemText(index, 1)
        item_price = self.search_list.GetItemText(index, 3).replace("Rs:", "")  # take selling price column
        self.item_id_hidden = self.search_list.GetItemData(index)
        self.item_code.SetValue(item_name)
        self.item_desc.SetValue(item_desc)
        self.item_price.SetValue(item_price)
        self.item_qty.SetFocus()

    def on_add_item(self, event):
        code = self.item_code.GetValue().strip()
        desc = self.item_desc.GetValue().strip()
        qty = self.item_qty.GetValue()
        if not code or not desc or qty < 1:
            wx.MessageBox("Please enter valid item details.", "Error", wx.ICON_ERROR)
            return
        # For demo, set price as 10.0 per item
        try:
            price = float(self.item_price.GetValue())
        except ValueError:
            wx.MessageBox("Invalid price entered.", "Error", wx.ICON_ERROR)
            return
        
        found = False
        for row in range(self.sales_list.GetItemCount()):
            if self.sales_list.GetItemText(row) == code:
                # Update existing item
                existing_qty = int(self.sales_list.GetItem(row, 2).GetText())
                new_qty = existing_qty + qty
                total = new_qty * price
                self.sales_list.SetItem(row, 2, str(new_qty))
                self.sales_list.SetItem(row, 4, f"Rs:{total:.2f}")
                found = True
                break

        if not found:
            # Insert new item
            total = qty * price
            idx = self.sales_list.InsertItem(self.sales_list.GetItemCount(), code)
            self.sales_list.SetItem(idx, 1, desc)
            self.sales_list.SetItem(idx, 2, str(qty))
            self.sales_list.SetItem(idx, 3, f"Rs:{price:.2f}")
            self.sales_list.SetItem(idx, 4, f"Rs:{total:.2f}")
            self.sales_list.SetItemData(idx,self.item_id_hidden)
        self.update_total()
        self.item_code.SetValue("")
        self.item_desc.SetValue("")
        self.item_qty.SetValue(1)
        self.item_code.SetFocus()
        

    def update_total(self):
        total = 0.0
        for i in range(self.sales_list.GetItemCount()):
            val = self.sales_list.GetItemText(i, 4).replace('Rs:', '')
            try:
                total += float(val)
            except ValueError:
                pass
        self.total_label.SetLabel(f"Total: Rs:{total:.2f}")

    def on_save_sale(self, event):
        if self.sales_list.GetItemCount() == 0:
            wx.MessageBox("No items to save.", "Info", wx.ICON_INFORMATION)
            return
        sale_date = self.date_picker.GetValue()  # wx.DateTime
        py_date = sale_date.FormatISODate()  # 'YYYY-MM-DD'
        sale_main_data = {"customer_name": self.cust_name.GetValue().strip() or "Walk-in",
                          "date":py_date,
                          "total": self.total_label.GetLabel().replace("Total: Rs:", "")}
        sale_id = save_sale(sale_main_data)
        items = []
        for i in range(self.sales_list.GetItemCount()):
            item_id = self.sales_list.GetItemData(i)
            qty = int(self.sales_list.GetItemText(i, 2))
            price = float(self.sales_list.GetItemText(i, 3).replace("Rs:", "").strip())
            items.append({"item_id": item_id, "qty": qty, "price": price})
        save_sale_items(sale_id, items)
        wx.MessageBox("Sale saved successfully!", "Success", wx.ICON_INFORMATION)
        self.on_clear(None)

    def on_clear(self, event):
        self.cust_name.SetValue("")
        self.item_code.SetValue("")
        self.item_desc.SetValue("")
        self.item_qty.SetValue(1)
        self.sales_list.DeleteAllItems()
        self.update_total()
