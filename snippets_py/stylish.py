#!/bin/python

# calls stylish-haskell on all files in specified relative folder
import sys
import os
import subprocess

dir = sys.argv[1]
fullpath = os.getcwd() + "/" + dir

for file in os.listdir(dir):
    if file.endswith("hs"):
        subprocess.run([f"stylish-haskell -i {fullpath}/{file}"], shell=True)
