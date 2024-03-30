import wx
from main_frame import MainFrame

class MyApp(wx.App):
    def OnInit(self):
        frame = MainFrame(None, title="VidCaptio")
        frame.Show()
        return True

if __name__ == "__main__":
    app = MyApp(False)
    app.MainLoop()
