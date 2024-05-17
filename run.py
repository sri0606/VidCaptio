import os
from gui.app import VidCaptioApp


if __name__ == '__main__':
    projects_dir = os.path.abspath('projects/')
    if not os.path.exists(projects_dir):
        os.makedirs(projects_dir)
    app = VidCaptioApp(projects_dir)
    app.start()