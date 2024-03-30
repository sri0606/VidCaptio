# ui/main_frame.py

import wx
# from core.video_processor import process_video

class MainFrame(wx.Frame):
    def __init__(self, *args, **kw):
        super(MainFrame, self).__init__(*args, **kw)

        self.InitUI()

    def InitUI(self):
        panel = wx.Panel(self)
        wx.StaticText(panel, label="Video Processing App", pos=(10, 10))

        # Example usage of core functionality
        # result = process_video("input_video.mp4")
        result = "Good job!"
        wx.StaticText(panel, label=result, pos=(10, 50))

        self.SetSize((400, 300))
        self.Centre()
