import webview
import webview.menu as wm
import subprocess
import platform
import os
import shutil
import time
from gui.api import VidCaptioAPI
from gui.utils import find_open_port


class VidCaptioApp:
    """
    App class for the VidCaptio application
    """
    def __init__(self,projects_dir):
        self.api = VidCaptioAPI()
        self.projects_dir = projects_dir

    def create_project(self,window):
        """
        Create a new project and upload a video file
        """
        file_types = ('Video Files (*.mp4)', 'All files (*.*)')
        result = window.create_file_dialog(webview.OPEN_DIALOG, allow_multiple=False, file_types=file_types)
        if result:
            original_file_path = result[0]
            print(f'Video uploaded: {original_file_path}')

            # Create a copy of the video file
            base_name = os.path.basename(original_file_path)
            filename,extension = os.path.splitext(base_name)

            # Create a new directory in the assets folder with the name of the file
            self.current_project_dir = os.path.join(self.projects_dir, filename)

            # If the directory already exists, append a number to the filename
            counter = 1
            while os.path.exists(self.current_project_dir):
                filename = f"{filename}_{counter}"
                self.current_project_dir = os.path.join(self.projects_dir, filename)
                counter += 1

            os.makedirs(self.current_project_dir, exist_ok=True)

            # Create the path to copy the file to
            copy_file_path = os.path.join(self.current_project_dir, "video"+extension)

            # Copy the file
            shutil.copy(original_file_path, copy_file_path)

            self.api.set_video_data(vid_path=original_file_path,vid_folder=os.path.join(self.projects_dir,filename),
                                    vid_extension=extension)
            # Send the URL of the video file to the loadVideo function
            url = f'http://localhost:{self.port}/{filename}/{"video"+extension}'
            window.evaluate_js(f'loadVideo("{url}")')

            self.save_project()
            return copy_file_path
        else:
            print('No video selected')
            return None

    def save_project(self):
        self.api.save_project_data()
        print('Save video clicked')

    def menu_action(self):
        print('Menu item clicked')

    def get_recent_projects(self):
        projects = [d for d in os.listdir(self.projects_dir) if os.path.isdir(os.path.join(self.projects_dir, d))]
        return projects

    def open_project(self,window):

        project_folders =self.get_recent_projects()

        window.evaluate_js(f'openProject({project_folders})')
        while True:
            result = window.evaluate_js('selectedProject')
            if result is not None:
                break
            time.sleep(0.1)  # Wait a bit before polling again to reduce CPU usage
        if result:
            self.current_project_dir = os.path.join(self.projects_dir,result)
            # Open the project...
            self.api.load_project_data(self.current_project_dir)

            vid_path = os.path.join(result, "video.mp4")
            
            vid_path = vid_path.replace('\\','/')
            # Send the URL of the video file to the loadVideo function
            url = f'http://localhost:{self.port}/{vid_path}'
            window.evaluate_js(f'loadVideo("{url}")')
            window.evaluate_js(f'loadCaptions("en")')
            are_captions_generated_js = str(self.api.are_captions_generated).lower()
            window.evaluate_js(f'loadProject({self.api.dest_languages},{self.api.captions_type},{are_captions_generated_js})')
    
    def reveal_project_location(self):
        file_loc = os.path.join(self.api.vid_folder,"video.mp4")
        # Open the directory of the video file
        if platform.system() == 'Windows':
            os.startfile(os.path.dirname(file_loc))
        elif platform.system() == 'Darwin':  # macOS
            subprocess.run(['open', os.path.dirname(file_loc)])
        else:  # Linux
            subprocess.run(['xdg-open', os.path.dirname(file_loc)])

    def reveal_file_location(self,file_name):
        try:
            file_loc = os.path.join(self.api.vid_folder,file_name)
            # Open the video file
            if platform.system() == 'Windows':
                os.startfile(file_loc)
            elif platform.system() == 'Darwin':  # macOS
                subprocess.run(['open', file_loc])
            else:  # Linux
                subprocess.run(['xdg-open', file_loc])
        except:
            self.reveal_project_location()

    def about_app(self):
        webview.create_window('About VidCaptio', 'gui/about.html')
    def start(self):
        """
        start the VidCaptio app
        """
        self.window = webview.create_window('VidCaptio', 'gui/index.html', js_api=self.api)

        self.window.events.closing += self.on_close
        self.port = find_open_port(8000, 8100)

        if self.port is None:
            print('No open port found')
        else:
            server = subprocess.Popen(['python', '-m', 'http.server', str(self.port)], cwd=self.projects_dir)

        menu_items = [
            wm.Menu('File', [
                wm.MenuAction('New Project',  lambda: self.create_project(self.window)),
                wm.MenuAction('Open recent Project', lambda: self.open_project(self.window)),
                wm.MenuAction('Save Project', lambda: self.save_project()),
            ]),
            wm.Menu('Open', [
                wm.MenuAction('Project folder',  lambda: self.reveal_project_location()),
                wm.MenuAction('Captioned video',  lambda: self.reveal_file_location("captioned.mp4")),
                wm.MenuAction('Transcript',  lambda: self.reveal_location("transcript.json")),
            ]),
            wm.Menu('About',[
                wm.MenuAction('About', lambda: self.about_app())
            ])
        ]

        webview.start(menu=menu_items)

    def on_close(self):
        self.api.save_project_data()
        print('Window closed')