import webview
import webview.menu as wm
import subprocess
import platform
import os
import shutil
import time
from gui.api import VidCaptioAPI
from gui.utils import find_open_port


class VidCaptioWindow:
    """
    window class for the VidCaptio application
    """
    def __init__(self,projects_dir,port,project_name=None):
        self.api = VidCaptioAPI()
        self.projects_dir = projects_dir
        self.port = port
        self.project_name = project_name

    def upload_video(self):
        """
        upload a video file
        """
        #if vid folder is not None, meaning a video is already uploaded
        if self.api.vid_folder:
            return
        
        file_types = ('Video Files (*.mp4)', 'All files (*.*)')
        result = self.window.create_file_dialog(webview.OPEN_DIALOG, allow_multiple=False, file_types=file_types)
        if result:
            original_file_path = result[0]
            print(f'Video uploaded: {original_file_path}')

            # Create a copy of the video file
            base_name = os.path.basename(original_file_path)
            filename,extension = os.path.splitext(base_name)
            self.project_name = filename
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
            self.window.evaluate_js(f'loadVideo("{url}")')

            self.video_upload = True
            self.save_project()
            return copy_file_path
        else:
            print('No video selected')
            return None

    def save_project(self):
        if self.api.vid_folder: 
            self.api.save_project_data()
            print('Save video clicked')

    def open_project(self,project_name):

        self.current_project_dir = os.path.join(self.projects_dir,project_name)
        # Open the project...
        self.api.load_project_data(self.current_project_dir)

        vid_path = os.path.join(project_name, "video.mp4")
        
        vid_path = vid_path.replace('\\','/')
        # Send the URL of the video file to the loadVideo function
        url = f'http://localhost:{self.port}/{vid_path}'
        self.window.evaluate_js(f'loadVideo("{url}")')
        self.window.evaluate_js(f'loadCaptions("en")')
        are_captions_generated_js = str(self.api.are_captions_generated).lower()
        self.window.evaluate_js(f'loadProject({self.api.dest_languages},{self.api.captions_type},{are_captions_generated_js})')

    def reveal_project_location(self):
        if self.api.vid_folder is None:
            return
        file_loc = os.path.join(self.api.vid_folder,"video.mp4")
        # Open the directory of the video file
        if  os.path.exists(file_loc):
            if platform.system() == 'Windows':
                os.startfile(os.path.dirname(file_loc))
            elif platform.system() == 'Darwin':  # macOS
                subprocess.run(['open', os.path.dirname(file_loc)])
            else:  # Linux
                subprocess.run(['xdg-open', os.path.dirname(file_loc)])

    def reveal_file_location(self,file_name):
        if self.api.vid_folder is None:
            return
        file_loc = os.path.join(self.api.vid_folder,file_name)
        # Open the directory of the file
        if os.path.exists(file_loc):
            try:
                # Open the video file
                if platform.system() == 'Windows':
                    os.startfile(file_loc)
                elif platform.system() == 'Darwin':  # macOS
                    subprocess.run(['open', file_loc])
                else:  # Linux
                    subprocess.run(['xdg-open', file_loc])
            except:
                self.reveal_project_location()

    def is_project_new(self):
        return self.project_name is None
    
    def start(self, window_title="New Project"):
        """
        start the VidCaptio app
        """
        self.window = webview.create_window(f'VidCaptio: {window_title}', 'gui/index.html', js_api=self.api,confirm_close=True)

        self.window.events.closing += lambda: self.save_project()

    def destroy(self):
        if hasattr(self, 'window'):
            self.window.destroy()

class VidCaptioApp:
    def __init__(self,projects_dir):
        self.port = find_open_port(8000, 8100)
        self.projects_dir = projects_dir
        server = subprocess.Popen(['python', '-m', 'http.server', str(self.port)], cwd=projects_dir)
        self.project_window = None

    def get_recent_projects(self):
        projects = [d for d in os.listdir(self.projects_dir) if os.path.isdir(os.path.join(self.projects_dir, d))]
        return projects

    def destroy_project_window(self):
        if self.project_window:
            self.project_window.destroy()
            self.project_window = None

    def create_window(self):
        #if project is being created from 
        if not self.project_window.project_name==-1 and self.project_window.is_project_new() :
            return
        temp_window = self.project_window
        self.project_window = VidCaptioWindow(self.projects_dir, self.port)
        self.project_window.start()
        if temp_window:
            temp_window.destroy()
        if self.app_window:
            self.app_window.destroy()
        return 

    def open_recent_project(self, project_name):
        #dont open the project if it is already open
        if project_name==self.project_window.project_name:
            return
        temp_window = self.project_window
        self.project_window = VidCaptioWindow(self.projects_dir, self.port,project_name=project_name)
        self.project_window.start(window_title=project_name)
        self.project_window.open_project(project_name=project_name)
        if temp_window:
            temp_window.destroy()
        if self.app_window:
            self.app_window.destroy()
        return

    def help_app(self):
        webview.create_window('About VidCaptio', 'gui/help.html')

    def start(self):
        self.app_window = webview.create_window('VidCaptio', 'gui/about.html')
        
        projects = self.get_recent_projects()

        # Create a new `VidCaptioWindow` instance to use in the menu actions
        self.project_window = VidCaptioWindow(self.projects_dir, self.port, project_name=-1)

        menu_items = [
            wm.Menu('Projects', [
                wm.MenuAction('New Project',  lambda: self.create_window()),
                wm.MenuSeparator(),
                  # Use `window` instance
                wm.MenuSeparator(),
                wm.Menu('Open recent Project', [
                    wm.MenuAction(project, lambda project=project: self.open_recent_project(project)) for project in projects
                ]),
            ]),
             wm.Menu('Current project', [
                    wm.MenuAction('Upload video', lambda: self.project_window.upload_video()),
                    wm.MenuAction('Save Project', lambda: self.project_window.save_project()),
                    wm.MenuSeparator(),
                    wm.MenuAction('Open folder location',  lambda: self.project_window.reveal_project_location()),
                    wm.MenuAction('Open Captioned video',  lambda:self.project_window.reveal_file_location("captioned.mp4")), 
                    wm.MenuAction('Open Transcript',  lambda: self.project_window.reveal_file_location("transcript.json")),
            ]),
            wm.Menu('Help',[
                wm.MenuAction('How to use', lambda: self.help_app())
            ])
        ]
 
        webview.start(menu=menu_items)