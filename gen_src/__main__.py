import importlib
import sys

from __init__ import berry_files
from python_src.berry_api import *
from python_src.berry_factory import berry_factory


# Main function called when running the project module
def main(argv):
    init_host(argv)
    berry_list = get_berry_list()
    berry_mod_list = {}
    berries = {}

    for berry_entry in berry_list:
        print('{}: {}'.format(berry_entry[1],berry_entry[0]))

    # Import all berry code files and store module references in dictionary with guid as key
    # The guid is retrieved as the value in the dictionary with the names of the berry files
    for name in berry_files:
        mod = importlib.import_module(name)
        berry_mod_list[berry_files[name]] = mod
        print(mod.__name__)

    # Create berry objects and store in dictionary. Register events
    for berry_entry in berry_list:
        berry_guid = berry_entry[0]
        if berry_guid in berry_mod_list:
            berry_module = berry_mod_list[berry_guid]
            berry_type = berry_entry[1]
            berry_name = berry_module.__name__
            berry = berry_factory(berry_name, berry_guid, berry_type)
            berries[berry.name] = berry  # Store berry reference in dictionary

            # If the berry has events, register the event handlers in the imported file to the events
            if hasattr(berry, 'events'):
                for event in berry.events.values():
                    handler = getattr(berry_module, event)
                    if not empty(handler):
                        getattr(berry, event)(handler)

    print(dir(berry_mod_list[berries['button1'].addr].__dict__))
    # Add all berry object references to the namespaces of all the imported berry files
    for mod in berry_mod_list.values():
        mod.__dict__.update(berries)

    # Spin while event-driven program runs
    while True:
        pass


if __name__ == '__main__':
    main(sys.argv)

