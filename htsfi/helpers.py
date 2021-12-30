import os
import glob
import shutil
from pathlib import Path

import matplotlib
{}
def update_style():
    mpldir = os.path.join(matplotlib.get_configdir(), 'stylelib')

    mplpath = Path(mpldir)
    if not mplpath.exists():
        mplpath.mkdir()

    PATH = os.getcwd()
    EXT = 'mplstyle'
    style_files = glob.glob(os.path.join(PATH, f'*.{EXT}'))

    for _path_file in style_files:
        _, fname = os.path.split(_path_file)
        dest = os.path.join(mpldir, fname)
        shutil.copy(_path_file, dest)
        
    matplotlib.pyplot.style.reload_library()
