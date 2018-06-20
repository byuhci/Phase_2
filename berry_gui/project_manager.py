import sys
import os
from berry_project import BerryProject
import camera
import cv2

from python_src.berry import Berry


class ProjectManager:
    def __init__(self, project_dir):
        self._set_project_(project_dir)
        self.project = None
        self.image = cv2.imread('background.jpg')
        self.berry_map = {}

    def _set_project_(self, project_dir):
        self.project_name = os.path.basename(project_dir)
        self.project_path = os.path.dirname(project_dir)
        # os.chdir(project_dir)

    def sync_project(self, project_dir=None):
        if project_dir is not None:
            self._set_project_(project_dir)

        self.project = BerryProject(self.project_name, self.project_path)
        self.project.sync_project()

    def find_berries(self, signal,class_to_find = Berry.BerryClasses.all):
        self.image, self.berry_map = camera.find_berries(self.project.berries,class_to_find)
        signal.emit()

    def current_image(self):
        return self.image

    def pick_berry(self, name):
        print('picked berry: {}'.format(name))
        return self.project.fetch_code(name)
