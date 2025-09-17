from pos_system.gui.sales_form import SalesForm
import wx

if __name__ == "__main__":
    app = wx.App(False)
    frame = SalesForm(None, "SINGHE LANKA TILE CENTER")
    app.MainLoop()
