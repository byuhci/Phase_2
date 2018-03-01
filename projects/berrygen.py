import os
import sys
from python_src import *
from python_src import berry_api as api
from python_src.berry_factory import berry_factory
import glob
import importlib
import shutil


class BerryProject:
    name = ''
    path = ''
    GEN_SRC_PATH = 'gen_src'
    MAIN_FILE_NAME = '__main__.py'
    INIT_FILE_NAME = '__init__.py'
    files = {'__main__.py': os.path.join(GEN_SRC_PATH, '__main__.py'),
             '__init__.py': os.path.join(GEN_SRC_PATH, '__init__.py')}

    def __init__(self, name, path=''):
        self.name = name
        self.path = os.path.join(path, name)
        if os.path.isdir(self.path):
            self._check_files_()
        else:
            self._gen_files_()

    def sync_berry(self):
        pass

    def sync_project(self):
        api.init_host(sys.argv)
        berry_list = api.get_berry_list()
        berry_mod_list = {}
        berries = {}
        files = self._get_module_files_()
        for name in files:
            mod = importlib.import_module(name)
            berry_mod_list[mod.guid] = mod
            print(mod.__name__)

    def _gen_files_(self):
        print('Making new project directory: {}'.format(self.path))
        os.makedirs(self.path)
        shutil.copyfile(os.path.join(self.GEN_SRC_PATH, self.INIT_FILE_NAME),
                        os.path.join(self.path, self.INIT_FILE_NAME))
        shutil.copyfile(os.path.join(self.GEN_SRC_PATH, self.MAIN_FILE_NAME),
                        os.path.join(self.path, self.MAIN_FILE_NAME))

    def _check_files_(self):
        pass

    def _get_module_files_(self):
        self.expr = '^(?!__).*\.py'
        files = glob.glob(os.path.join(self.path, self.expr))
        print(files)
        return files


def main(argv):
    if len(argv) < 2:
        print('Must pass project name as parameter')
        return
    if len(argv) > 2:
        proj = BerryProject(argv[1], argv[2])
    else:
        proj = BerryProject(argv[1], 'projects')
    proj.sync_project()


if __name__ == '__main__':
    main(sys.argv)
