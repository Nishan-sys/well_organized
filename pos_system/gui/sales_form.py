import wx
from ..services.sales_service import add_item_to_sale, save_sale
import wx.adv 

class SalesForm(wx.Frame):
    def __init__(self, parent, title):
        super().__init__(parent, title=title, size=(850, 700))

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
        cust_box = wx.StaticBox(self.panel, label="Customer Info")
        cust_box.SetForegroundColour('#1e8449')
        cust_sizer = wx.StaticBoxSizer(cust_box, wx.HORIZONTAL)
        cust_grid = wx.FlexGridSizer(2, 2, 10, 10)
        cust_grid.Add(wx.StaticText(self.panel, label="Customer Name:"), 0, wx.ALIGN_CENTER_VERTICAL)
        self.cust_name = wx.TextCtrl(self.panel)
        cust_grid.Add(self.cust_name, 1, wx.EXPAND)
        cust_grid.Add(wx.StaticText(self.panel, label="Date:"), 0, wx.ALIGN_CENTER_VERTICAL)
        self.date_picker = wx.adv.DatePickerCtrl(self.panel)
        cust_grid.Add(self.date_picker, 1, wx.EXPAND)
        cust_sizer.Add(cust_grid, 1, wx.ALL | wx.EXPAND, 10)
        main_sizer.Add(cust_sizer, 0, wx.ALL | wx.EXPAND, 15)

        # Item Entry
        item_box = wx.StaticBox(self.panel, label="Add Item")
        item_box.SetForegroundColour('#b9770e')
        item_sizer = wx.StaticBoxSizer(item_box, wx.HORIZONTAL)
        item_grid = wx.FlexGridSizer(1, 8, 10, 10)
        item_grid.Add(wx.StaticText(self.panel, label="Item Code/Name:"), 0, wx.ALIGN_CENTER_VERTICAL)
        self.item_code = wx.TextCtrl(self.panel)
        item_grid.Add(self.item_code, 1, wx.EXPAND)
        #self.item_code.Bind(wx.EVT_TEXT, self.on_search)
        #self.item_code.Bind(wx.EVT_KILL_FOCUS, self.on_leave)
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
        self.search_list.InsertColumn(0, "Item Name", width=150)
        self.search_list.InsertColumn(1, "Description", width=250)
        self.search_list.InsertColumn(2, "Cost", width=100)
        self.search_list.InsertColumn(3, "Price", wx.LIST_FORMAT_RIGHT, 100)

        search_sizer.Add(self.search_list, 1, wx.ALL | wx.EXPAND, 5)
        self.search_list.SetMinSize(( -1, 60 ))
        main_sizer.Add(search_sizer, 1, wx.ALL | wx.EXPAND, 10)
        #self.search_list.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.on_search_item_click) 


        # Sales List
        list_box = wx.StaticBox(self.panel, label="Sales Items")
        list_box.SetForegroundColour('#2874a6')
        list_sizer = wx.StaticBoxSizer(list_box, wx.VERTICAL)
        self.sales_list = wx.ListCtrl(self.panel, style=wx.LC_REPORT | wx.BORDER_SUNKEN)
        self.sales_list.InsertColumn(0, "Item Code", width=90)
        self.sales_list.InsertColumn(1, "Description", width=180)
        self.sales_list.InsertColumn(2, "Qty", wx.LIST_FORMAT_CENTER, 60)
        self.sales_list.InsertColumn(3, "Price", wx.LIST_FORMAT_RIGHT, 80)
        self.sales_list.InsertColumn(4, "Total", wx.LIST_FORMAT_RIGHT, 80)
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
        #self.add_btn.Bind(wx.EVT_BUTTON, self.on_add_item)
        #self.save_btn.Bind(wx.EVT_BUTTON, self.on_save_sale)
        #self.clear_btn.Bind(wx.EVT_BUTTON, self.on_clear)
        #self.populate_product_list()
        self.Centre()
        self.Show()

    def on_add_item(self, event):
        # Example data from GUI inputs
        item_code = "A101"
        qty = 2
        add_item_to_sale(item_code, qty)

    def on_save(self, event):
        save_sale()
