#Brainstorm program layout

class BerryProject:



    def __init__(self, project_name, path=DEFAULT):
        #if not exists, create project

    def sync_project(self):
        #init_host
        #talk to berries
        #verify and create berry stub files

    def get_berry_file(self, berry_name):
        return file_name

# berry_detector

def detect_berries(berry_list):
    found_berries = {} # berry_name,
    contour_list = get_all_contours()
    for berry in berry_list:
        c = find_berry(berry, contour_list)
        found_berries[berry] = c
    return found_berries


def find_berry(single_berry, contour_list):
    # take 2 images, with light and without
    # subtract and find light inside contour
    return contour


def get_all_contours():
    # black and white
    #
    return contours



# main file
# setup and controlling logic
#   Functions for

file_name = get_berry_file('button1')
with open(file_name) as f:
    text = f.read()
    print(text)



# GUI file
