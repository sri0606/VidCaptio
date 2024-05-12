import webview
import webview.menu as wm
import subprocess
import os
import shutil
from gui.api import VidCaptioAPI
from gui.utils import find_open_port


class VidCaptioApp:
    """
    App class for the VidCaptio application
    """
    def __init__(self):
        self.api = VidCaptioAPI()
        
    def upload_video(self,window):
        file_types = ('Video Files (*.mp4;*.avi;*.mkv)', 'All files (*.*)')
        result = window.create_file_dialog(webview.OPEN_DIALOG, allow_multiple=False, file_types=file_types)
        if result:
            original_file_path = result[0]
            print(f'Video uploaded: {original_file_path}')

            # Create a copy of the video file
            base_name = os.path.basename(original_file_path)
            filename,extension = os.path.splitext(base_name)
            # Create a new directory in the assets folder with the name of the file
            new_dir_path = os.path.join(os.path.abspath('assets/'), filename)
            os.makedirs(new_dir_path, exist_ok=True)

            # Create the path to copy the file to
            copy_file_path = os.path.join(new_dir_path, "video"+extension)

            # Copy the file
            shutil.copy(original_file_path, copy_file_path)

            self.api.set_video_data(vid_path=original_file_path,vid_folder=f"assets/{filename}",vid_extension=extension)
            # Send the URL of the video file to the loadVideo function
            url = f'http://localhost:{self.port}/{filename}/{"video"+extension}'
            window.evaluate_js(f'loadVideo("{url}")')
            return copy_file_path
        else:
            print('No video selected')
            return None

    def save_video(self):
        print('Save video clicked')

    def menu_action(self):
        print('Menu item clicked')

    def start(self):
        """
        start the VidCaptio app
        """
        window = webview.create_window('VidCaptio', 'gui/index.html', js_api=self.api)

        self.port = find_open_port(8000, 8100)

        if self.port is None:
            print('No open port found')
        else:
            server = subprocess.Popen(['python', '-m', 'http.server', str(self.port)], cwd='assets')

        menu_items = [
            wm.Menu('File', [
                wm.MenuAction('Upload video',  lambda: self.upload_video(window)),
                wm.MenuAction('Save video', self.save_video),
            ]),
            wm.Menu('Edit', [
                wm.MenuAction('Cut', self.menu_action),
                wm.MenuAction('Copy', self.menu_action),
                wm.MenuAction('Paste', self.menu_action),
            ]),
            wm.Menu('About',[
                wm.MenuAction('About', self.menu_action)
            ])
        ]

        webview.start(menu=menu_items)

    def on_close(self):
        print('Window closed')