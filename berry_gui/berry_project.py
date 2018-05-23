import os
import sys
from python_src import *
from python_src import berry_api as api
from python_src.berry_factory import berry_factory
import glob
import importlib
import importlib.util
import shutil
import re
from os.path import join


class BerryProject:
    GEN_SRC_PATH = '../gen_src'
    MAIN_FILE_NAME = '__main__.py'
    INIT_FILE_NAME = '__init__.py'
    src_files = {'__main__.py': join(GEN_SRC_PATH, '__main__.py'),
                 '__init__.py': join(GEN_SRC_PATH, '__init__.py'),
                 'RGB': join(GEN_SRC_PATH, 'light-src.py'),
                 'Button': join(GEN_SRC_PATH, 'button-src.py'),
                 'Knob': join(GEN_SRC_PATH, 'knob-src.py'),
                 'Slider': join(GEN_SRC_PATH, 'slider-src.py'),
                 'Pressure': join(GEN_SRC_PATH, 'pressure-src.py'),
                 'Vibrerry': join(GEN_SRC_PATH, 'buzz-src.py'),
                 'Beeper': join(GEN_SRC_PATH, 'beeper-src.py'),
                 'Servo': join(GEN_SRC_PATH, 'servo-src.py'),
                 'Flex': join(GEN_SRC_PATH, 'flex-src.py')
                 }
    default_names = {
        'RGB': 'light{}',
        'Button': 'button{}',
        'Knob': 'knob{}',
        'Slider': 'slider{}',
        'Pressure': 'pressure{}',
        'Vibrerry': 'buzz{}',
        'Beeper': 'beeper{}',
        'Servo': 'servo{}',
        'Flex': 'flex{}'
    }

    '''
    project_name is also the folder inside the path where all the files are located
    project_init is a module reference to the __init__.py, which enables fetching the 
        berry_files field.  That field holds the currently known berry files
    project_files is the local reference to project_init.berry_files dict
    project_berries is refreshed after each call to sync_project and holds references 
        to all the berry objects, keyed by the berry's name
    '''
    def __init__(self, name, path=''):
        self.project_name = name
        self.path = path
        self.fullpath = os.path.join(self.path, self.project_name)
        sys.path.insert(0, self.path)
        self.project_init = importlib.import_module(self.project_name)
        self.project_files = None
        self.project_berries = {}

        self._check_files_()

    def sync_berry(self):
        pass

    @property
    def berries(self):
        return self.project_berries

    def sync_project(self):
        api.init_host(sys.argv)
        berry_list = api.get_berry_list()
        self.project_berries.clear()
        self.project_files = self.project_init.berry_files

        # This is how you get the module from here:
        # package = '.{}'.format(file)
        # mod = importlib.import_module(package, self.project_name)

        # For each berry from the network, see if the guid is present in the project files dict
        #   If not, make a new file with a generic name and add it both to the project files dict
        #   and the persistent project __init__.py field via self._update_project_files_()
        for berry_inst in berry_list:
            guid = berry_inst[0]
            berry_type = berry_inst[1]
            if guid in self.project_files.keys():
                name = self.project_files[guid]
            else:
                name = self._make_berry_file(berry_type)
                self.project_files[guid] = name
                self._update_project_files_()
            berry = berry_factory(name, guid, berry_type)
            self.project_berries[name] = berry

    def fetch_code(self, name):
        return join(self.fullpath, ''.join((name, '.py')))

    def run_project(self):
        self.project_init.reload()
        self.project_init.__main__.main(sys.argv)

    def _update_project_files_(self):
        with open(self.src_files[self.INIT_FILE_NAME], 'r') as file:
            init_text = file.read()
        init_text = init_text.format(files=str(self.project_files))
        with open(join(self.fullpath, self.INIT_FILE_NAME), 'w') as file:
            file.write(init_text)

    def _make_berry_file(self, berry_type, nameset=None):
        if nameset is None:
            nameset = self.project_files

        src_file = join(self.GEN_SRC_PATH, self.src_files[berry_type])
        for n in range(1, 999):
            name = self.default_names[berry_type].format(n)
            if name not in nameset:
                break
        filename = join(self.fullpath, ''.join([name, '.py']))
        shutil.copyfile(src_file, filename)
        return name

    def _gen_files_(self):
        print('Making new project directory: {}'.format(self.fullpath))
        os.makedirs(self.fullpath, exist_ok=True)
        shutil.copyfile(join(self.GEN_SRC_PATH, self.INIT_FILE_NAME),
                        join(self.fullpath, self.INIT_FILE_NAME))
        shutil.copyfile(join(self.GEN_SRC_PATH, self.MAIN_FILE_NAME),
                        join(self.fullpath, self.MAIN_FILE_NAME))

    def _check_files_(self):
        if not os.path.exists(self.fullpath) or not os.listdir(self.fullpath):
            self._gen_files_()
            return
        if not (os.path.exists(join(self.fullpath, self.INIT_FILE_NAME)) and os.path.exists(
                join(self.fullpath, self.MAIN_FILE_NAME))):
            print('main and/or init module files not found, please remake project')
            return

        current_berry_files = ['{}.py'.format(f) for f in self.project_init.berry_files.values()]
        current_berry_files.sort()
        files = self._get_module_files_()
        files.sort()
        print('Project-aware berry files:')
        print(current_berry_files)
        print('System-detected berry files:')
        print(files)
        if files == current_berry_files:
            print('Project state verified')
        else:
            diff = set(current_berry_files).difference(set(files))
            if not len(diff) != 0:
                print('Expected file{} not found:'.format('' if len(diff) == 1 else 's'))
                print(*diff)
            diff = set(files).difference(set(current_berry_files))
            if len(diff) != 0:
                print('Unexpected file{} found:'.format('' if len(diff) == 1 else 's'))
                print(*diff)

    def _get_module_files_(self):
        expr = r'^(?!__).*'
        search_path = os.path.join(self.fullpath, '*')

        # files = [os.path.splitext(os.path.basename(name))[0] for name in glob.glob(search_path)]
        files = [os.path.basename(name) for name in glob.glob(search_path)]
        regex = re.compile(expr)
        filter_files = list(filter(regex.search, files))
        print(files)
        print(filter_files)
        return filter_files


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
    print(sys.path)
    main(sys.argv)
