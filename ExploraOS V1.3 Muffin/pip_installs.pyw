import os
from os import system as command
import subprocess
import sys
import time
import ctypes
from pathlib import Path


def install_pip():


    try:
        from PIL import Image
        print("pillow is already installed.")
        
    except ImportError:
        print("One of the python PIPs haven't been installed yet. Here are the required pips that will be installed :")
        print("CustomTkinter, Pillow, elevate")
        print("/!\ Dont worry, we'll only use 'pip install [pip name]' /!\!")
        print("-----------------------------------")

        time.sleep(4)
        print("pillow is not installed. Installing now...")

        subprocess.check_call([sys.executable, "-m", "pip", "install", "pillow"])
        print("pillow has been installed.")



 

      

    try:
        import customtkinter
        print("customtkinter is already installed.")
        
    except ImportError:
        print("customtkinter is not installed. Installing now...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "customtkinter"])
        print("customtkinter has been installed.")

    try:
        import keyboard
        print("keyboard is already installed.")
        
    except ImportError:
        print("keyboard is not installed. Installing now...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "keyboard"])
        print("keyboard has been installed.")

    try:
        import elevate
        print("elevate is already installed.")
        
    except ImportError:
        print("elevate is not installed. Installing now...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "elevate"])
        print("elevate has been installed.")

    try:
        import requests
        print("requests is already installed.")
        
    except ImportError:
        print("requests is not installed. Installing now...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
        print("requests has been installed.")

install_pip()
        