import wx
import wx.media

class VideoPlayerWidget(wx.Panel):
    def __init__(self, parent, pos=(100, 100), size=(400, 300)):
        super().__init__(parent, pos=pos, size=size)

        self.media = wx.media.MediaCtrl(self, style=wx.SIMPLE_BORDER)

        # Load a placeholder image and set it as the background
        image = wx.Image("assets/video_placeholder.jpg", wx.BITMAP_TYPE_ANY)
        bitmap = wx.Bitmap(image)
        self.placeholder = wx.StaticBitmap(self, bitmap=bitmap, style=wx.SIMPLE_BORDER)
        self.placeholder.Hide()

        # Add a play/pause button
        self.play_pause_button = wx.Button(self, label='Play', style=wx.SIMPLE_BORDER)
        self.play_pause_button.Bind(wx.EVT_BUTTON, self.on_play_pause)

        # Add a slider as a time bar
        self.slider = wx.Slider(self, -1, 0, 0, 1000, style=wx.SIMPLE_BORDER)
        self.slider.Bind(wx.EVT_SLIDER, self.on_seek)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.media, 1, wx.EXPAND)
        sizer.Add(self.play_pause_button, 0, wx.CENTER)
        sizer.Add(self.slider, 0, wx.EXPAND)
        self.SetSizer(sizer)

    def load_video(self, filepath):
        if self.media.Load(filepath):
            self.media.SetInitialSize()
            self.GetSizer().Layout()
            self.play_pause_button.Enable(True)
            self.placeholder.Hide()
        else:
            wx.MessageBox("Unable to load %s: Unsupported format?" % filepath,
                          "ERROR",
                          wx.ICON_ERROR | wx.OK)
            self.placeholder.Show()

    def play_video(self):
        self.media.Play()

    def on_play_pause(self, event):
        if self.media.GetState() == wx.media.MEDIASTATE_PLAYING:
            self.media.Pause()
            self.play_pause_button.SetLabel('Play')
        else:
            self.media.Play()
            self.play_pause_button.SetLabel('Pause')

    def on_seek(self, event):
        offset = self.slider.GetValue()
        self.media.Seek(offset * self.media.Length() // 1000)
