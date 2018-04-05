


def generste_unuiqe_file_for_each_berry(berry_type):

    file = None

    file = open(berry_type + "_editor.txt","w")

    
    file.close()

    return file