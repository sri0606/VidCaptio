# ui/main_frame.py

import wx
from video_player_widget import VideoPlayerWidget
import wx.media
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

        # Create a panel for the left sizer and set its background color
        left_panel = wx.Panel(panel)
        left_panel.SetBackgroundColour('blue')

        self.video_player = VideoPlayerWidget(left_panel,pos=(10, 50), size=(400, 300))
        # Add a button for uploading a file
        upload_button = wx.Button(left_panel, label='Upload Video', pos=(10, 410))
        upload_button.Bind(wx.EVT_BUTTON, self.on_open_file)

        left_sizer = wx.BoxSizer(wx.VERTICAL)
        left_sizer.Add((50, 100))  # Add some padding at the top
        left_sizer.Add(self.video_player, 5, wx.EXPAND)
        left_sizer.Add((10, 10))  # Add some padding at the bottom
        left_sizer.Add(upload_button, 1, wx.CENTER)
        left_panel.SetSizer(left_sizer)

        # Create a panel for the right sizer and set its background color
        right_panel = wx.Panel(panel)
        right_panel.SetBackgroundColour('green')

         # Add a button for generating captions
        generate_button = wx.Button(right_panel, label='Generate Captions',pos=(810, 10))
        # Bind an event handler to the button
        generate_button.Bind(wx.EVT_BUTTON, self.on_generate_captions)

        right_sizer = wx.BoxSizer(wx.VERTICAL)
        right_sizer.Add((50, 100))  # Add some padding at the top
        right_sizer.Add(generate_button, 1, wx.CENTER)
        right_panel.SetSizer(right_sizer)

        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        main_sizer.Add(left_panel, 3, wx.EXPAND | wx.ALL, 5)
        main_sizer.Add(right_panel, 1, wx.EXPAND | wx.ALL, 5)

        panel.SetSizer(main_sizer)
        self.SetSize((1200, 700))
        self.Centre()

    def on_open_file(self, event):
        wildcard = "MP4 files (*.mp4)|*.mp4"
        dialog = wx.FileDialog(self, "Open Video File", wildcard=wildcard,
                            style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)

        if dialog.ShowModal() == wx.ID_CANCEL:
            return     # the user changed their mind

        # Proceed loading the file chosen by the user
        pathname = dialog.GetPath()
        self.video_player.load_video(pathname)
        self.video_player.play_video()

        # Call Layout on the sizer to ensure the MediaCtrl widget is resized correctly
        self.video_player.Layout()

    def on_generate_captions(self, event):
        # Placeholder for generating captions
        wx.MessageBox("Captions generated!", "Success", wx.OK | wx.ICON_INFORMATION)