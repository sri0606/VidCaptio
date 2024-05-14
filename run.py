import os
import webview
import webvtt
import pysrt
import stable_whisper
from gui.app import VidCaptioApp
import logging

logging.basicConfig(filename='app.log', level=logging.DEBUG)

if __name__ == '__main__':
    logging.info('Starting application')
    projects_dir = os.path.abspath('projects/')
    logging.info('Projects directory: %s', projects_dir)
    if not os.path.exists(projects_dir):
        os.makedirs(projects_dir)
    app = VidCaptioApp(projects_dir)
    logging.info('Created VidCaptioApp')
    app.start()
    logging.info('Started VidCaptioApp')
    app.start()