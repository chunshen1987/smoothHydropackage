#! /usr/bin/env python

import shutil
from os import path
import subprocess

hdf5_version = '1.8.13'

def install_hdf5(install_path):
    scr_path = path.abspath('./hdf5-%s' % hdf5_version)
    if path.exists(scr_path):
        shutil.rmtree(scr_path)
    p = subprocess.Popen('./configure --prefix=%s ' % install_path
                         + '--enable-fortran --enable-cxx', shell=True,
                         cwd=scr_path)
    p.wait()
    p = subprocess.Popen('make', shell=True, cwd=scr_path)
    p.wait()
    p = subprocess.Popen('make check', shell=True, cwd=scr_path)
    p.wait()
    p = subprocess.Popen('make install', shell=True, cwd=scr_path)
    p.wait()

if __name__ == "__main__":
    folder_path = path.abspath('./hdf5')
    install_hdf5(folder_path)