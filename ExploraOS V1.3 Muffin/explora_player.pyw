import os
from os import system

script_dir = os.path.dirname(os.path.realpath(__file__))
os.chdir(script_dir)

system("pythonw main.pyw")