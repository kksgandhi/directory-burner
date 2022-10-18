# Copy this file to config.py and edit it to your heart's content

import os
from os import path

def remove_function(directory, filename):
    """
    This function does the actual removal
    normally this uses os.remove, but feel free to 
    replace it with a trash function or similar
    """
    os.remove(path.join(directory, filename))
