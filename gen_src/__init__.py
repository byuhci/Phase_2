# __all__ = ['berry_files']
import importlib
from . import __main__

berry_files = { }
berry_mods = dict()
package_module = importlib.__import__(__name__)

for guid, name in berry_files.items():
    mod = importlib.import_module('.' + name, __package__)
    berry_mods[name] = mod
    print(mod.__name__)


def reload():
    global package_module
    global berry_mods
    package_module = importlib.reload(package_module)
    for name, mod in berry_mods.items():
        berry_mods[name] = importlib.reload(mod)
