# Copyright (C) 2024 ExploraOS
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.


import tkinter as tk
from tkinter import messagebox
import traceback
import customtkinter as ctk
import webbrowser
from PIL import Image, ImageTk
from customtkinter import filedialog
import requests
import sys
import os
from os import system
from time import sleep as wait
import threading


script_dir = os.path.dirname(os.path.realpath(__file__))
favicon = os.path.join(script_dir, "exploraOSicon.ico")
data_dir = os.path.join(script_dir, "data")
imgdir = os.path.join(script_dir, "images")
fontBold = ("Arial", 12, "bold")
Defaultfont = ("Arial", 24)

currentframe = None
havecurrentframe = False
hasframeopen = False
currentframename = ""

desktop_content = None
shortcut_btn = None
boot_btn = None
bootinfo_btn = None
fullscreen = None

updateavailable = None
spawnupdateinfo = True

frame_label = None

textbox = None
notepad_current_file = None

taskbar_home_frame = None
taskbar = None
home_topbar = None


# data variables
theme = ""
cancreateshortcut = ""
canbootanim = ""
bootinfo = ""

haveshowerror = ""

# Data files
theme_file = os.path.join(data_dir, "theme.txt")
create_shortcut_file = os.path.join(data_dir, "createshortcut.txt")
boot_file = os.path.join(data_dir, "boot.txt")
bootinfo_file = os.path.join(data_dir, "bootinfo.txt")

haveshowerror_file = os.path.join(data_dir, "updates", "haveshownerror.txt")

def checkupdate():
 global updateavailable
 url = "https://rediblesky.is-a.dev/expUpdatesResponse"
 response = requests.get(url)

 if 'true' in response.text:
  print("update available!")
  updateavailable = True
 else:
  print("no updates available!")
  updateavailable = False

def restart():
 exit()


def boot():
 global theme
 global cancreateshortcut
 global canbootanim
 global bootinfo
 global haveshowerror
 frame = tk.Frame(window, bg="black")
 frame.pack(fill=tk.BOTH, expand=True)
 label = tk.Label(frame, text="ExploraOS is booting", font=fontBold, fg="white", bg=frame["bg"])
 label.pack(pady=470)
 wait(2)
 checkupdate()
 with open(boot_file, "r") as file:
  content3 = file.read()
  canbootanim = content3

 with open(bootinfo_file, "r") as file:
  content4 = file.read()
  bootinfo = content3

 with open(create_shortcut_file, "r") as file:
  content2 = file.read()
  print(content2)
  cancreateshortcut = content2

 with open(haveshowerror_file, "r") as file:
  content5 = file.read()
  print(content5)
  haveshowerror = content5


 

 if cancreateshortcut == "true":
  os.chdir(script_dir)
  system("create_shortcut.js")


 with open(theme_file, "r") as file:
  content = file.read()
  print(content)
  theme = content

 if canbootanim == "true":
 
  wait(1)
  label.destroy()
  imageFile = Image.open(os.path.join(script_dir, "exploraOSicon.ico"))
  imagePhoto = ImageTk.PhotoImage(imageFile)
  image = tk.Label(frame, image=imagePhoto, bg=frame["bg"])
  image.image = imagePhoto
  image.pack(pady=300)
  if updateavailable == True:
   label2 = tk.Label(frame, text="Update detected.", font=fontBold, bg=frame["bg"], fg="white")
   label2.pack()
  wait(5)
  frame.destroy()
  load_desktop()
 else:
    frame.destroy()
    load_desktop()

def fullscreen_switch():
 global fullscreen
 if fullscreen == True:
  window.attributes("-fullscreen", False)
  fullscreen = False
 elif fullscreen == False:
  window.attributes("-fullscreen", True)
  fullscreen = True
 

# data functions 
def switch_theme():
 global theme
 print(f"old theme : {theme}")
 with open(theme_file, "w") as file:

  
  if theme == "white":
    file.write("black")
    theme = "black"
  elif theme == "black":
    file.write("white")
    theme = "white"

  print(f"Current theme : {theme}")

  for childrens in desktop_content.winfo_children():
   childrens.destroy()
  reload_desktop("", "")

def switch_create_shortcut():
 global cancreateshortcut
 global shortcut_btn
 print(f"old create_shortcut : {cancreateshortcut}")
 with open(create_shortcut_file, "w") as file:
  if cancreateshortcut == "true":
   file.write("false")
   cancreateshortcut = "false"
  elif cancreateshortcut == "false":
   file.write("true")
   cancreateshortcut = "true"
 print(f"current create_shortcut : {cancreateshortcut}")
 shortcut_btn.configure(text=f"Create shortcut when booted (current : {cancreateshortcut})")

def switch_boot():
 global canbootanim
 global boot_btn
 print(f"old bootscreen : {canbootanim}")
 with open(boot_file, "w") as file:
  if canbootanim == "true":
   file.write("false")
   canbootanim = "false"
  elif canbootanim == "false":
   file.write("true")
   canbootanim = "true"
 print(f"current bootscreen : {canbootanim}")
 boot_btn.configure(text=f"Boot screen (current : {canbootanim})")

def switch_boot_info():
 global bootinfo
 global bootinfo_btn
 print(f"old bootinfo : {bootinfo}")
 with open(bootinfo_file, "w") as file:
  if bootinfo == "true":
   file.write("false")
   bootinfo = "false"
  elif bootinfo == "false":
   file.write("true")
   bootinfo = "true"
 print(f"current boot info : {bootinfo}")
 bootinfo_btn.configure(text=f"Boot info (current : {bootinfo})")
 

# end of data functions
 
def options_callback(choice):
 global textbox
 global frame_label
 global notepad_current_file
 if choice == "New":
  textbox.delete("0.0", "end")
 elif choice == "Open":
  response = filedialog.askopenfilename(title="Select a file", filetypes=[(".txt", " *.txt")])

  if response:
   notepad_current_file = response
   with open(notepad_current_file, "r") as file:
    content = file.read()
    textbox.delete("0.0", "end")
    textbox.insert("0.0", content)

    frame_label.configure(text=notepad_current_file)
    
 elif choice == "Save":
  if notepad_current_file == None:
   print("not selected")
   saved_response = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])

   if saved_response:
    with open(saved_response, "w") as file:
     file.write(textbox.get("0.0", "end-1c"))
     frame_label.configure(text=saved_response)
     notepad_current_file = saved_response
  else:
   with open(notepad_current_file, "w") as file:
     file.write(textbox.get("0.0", "end-1c"))
     frame_label.configure(text=notepad_current_file)
     
    


 

def close_function():
 global hasframeopen
 currentframe.destroy()
 hasframeopen = False
 
def create_frame(framename):
 global currentframename
 global hasframeopen
 global currentframe
 global shortcut_btn
 global textbox
 global frame_label
 global boot_btn
 global bootinfo_btn
 global havecurrentframe

 taskbar_home_frame.pack_forget()

 if havecurrentframe == True:
  currentframe.destroy()

 havecurrentframe = True
 hasframeopen = True
 currentframename = framename

 frame = ctk.CTkFrame(desktop_content, width=900, height=450, corner_radius=0)
 frame.pack_propagate(False)
 frame.pack(pady=170)
 currentframe = frame

 topbar = ctk.CTkFrame(frame, height=70, corner_radius=0)
 topbar.pack_propagate(False)
 topbar.pack(fill="x", side="top")

 

 closebtn = ctk.CTkButton(topbar, width=50, height=50, command=close_function, text="X")
 closebtn.pack(side="right")

 frame_label = ctk.CTkLabel(topbar, text=framename, font=fontBold)
 frame_label.pack(side="left")

 if framename == "Settings":
  shortcut_btn = ctk.CTkButton(frame, text=f"Create shortcut when booted (current : {cancreateshortcut})", corner_radius=16, command=switch_create_shortcut)
  shortcut_btn.pack(pady=(0,20))
  boot_btn = ctk.CTkButton(frame, text=f"Boot screen (current : {canbootanim})", corner_radius=16, command=switch_boot)
  boot_btn.pack(pady=(0,20))
  bootinfo_btn = ctk.CTkButton(frame, text=f"Boot info (closed for maintenance)", corner_radius=16)
  bootinfo_btn.pack(pady=(0,20))
  fullscreen_btn = ctk.CTkButton(frame, text=f"Fullscreen toggle", corner_radius=16, command=fullscreen_switch)
  fullscreen_btn.pack(pady=(0,20))
 if framename == "Explora Version":
  label1 = ctk.CTkLabel(frame, text="Exp Ver : 1.3", font=fontBold)
  label1.pack(pady=100)
 if framename == "Notepad":
  
  textbox = ctk.CTkTextbox(frame, corner_radius=16, height=300, width=600)
  textbox.insert("0.0", "Type something...")
  textbox.pack(side="right")

  options = ctk.CTkOptionMenu(frame, corner_radius=0, fg_color=("#818281", "#717171"), dropdown_fg_color=("#717171", "#717171"), button_color=("#5A5B5A", "#5A5B5A"), button_hover_color=("#484948", "#484948"), values=["New", "Save", "Open"], command=options_callback)
  options.pack(fill="x", side="top")
 
  







## windows
def test_window():
 create_frame("Test window")
def settings_window():
 create_frame("Settings")
def error_window():
 create_frame("error")
def expver_window():
 create_frame("Explora Version")
def notepad_window():
 create_frame("Notepad")
 
def taskbar_home():
 global taskbar
 global home_topbar
 global taskbar_home_frame
 taskbar_home_frame.pack(side="bottom", pady=(0, 20))
 taskbar_home_frame.configure(fg_color=taskbar["bg"])

 if havecurrentframe == True:
  currentframe.destroy()

 home_topbar.configure(bg=taskbar["bg"])
 

def tb_home_close_func():
 taskbar_home_frame.pack_forget()



def load_desktop():
 global spawnupdateinfo
 global desktop_content
 global taskbar_home_frame
 global home_topbar
 global taskbar

 global haveshowerror
 if updateavailable == True:
  if spawnupdateinfo == True:
   if haveshowerror == "false":
    result = messagebox.askquestion("Update available", "We detected a update.\nRedirect to 'https://rediblesky.is-a.dev/ExploraOS.zip' ?")
    spawnupdateinfo = False
    haveshowerror == "true"
    with open(haveshowerror_file, "w") as file:
     file.write("true")
    if result == 'yes':
     webbrowser.open("https://rediblesky.is-a.dev/ExploraOS.zip")

 taskbar_home_frame = ctk.CTkFrame(desktop_content, height=750, width=800, corner_radius=16)
 taskbar_home_frame.pack_propagate(False)
 
 

 taskbar = tk.Frame(desktop_content, height=50)
 taskbar.pack_propagate(False)
 taskbar.pack(fill="x", side="bottom")

 imagefile = Image.open(os.path.join(script_dir, "exploraOSiconrounded.png"))
 imagefile = imagefile.resize((28, 50), Image.LANCZOS)
 imagephoto = ctk.CTkImage(light_image=imagefile, dark_image=imagefile) #ImageTk.PhotoImage(imagefile)
 
 home_btn = ctk.CTkButton(taskbar, image=imagephoto, corner_radius=0, width=28, text="Home", command=taskbar_home)
 home_btn.pack(side="left", fill="y", padx=(0, 20))

 home_topbar = tk.Frame(taskbar_home_frame, height=60)
 home_topbar.pack(side="top", fill="x")
 home_topbar.pack_propagate(False)

 home_close_btn = ctk.CTkButton(home_topbar, corner_radius=0, width=58, text="X", command=tb_home_close_func)
 home_close_btn.pack(side="right", fill="y")

 home_label_title = ctk.CTkLabel(home_topbar, text="Home", font=Defaultfont)
 home_label_title.pack(side="left")

 home_image_file = Image.open(os.path.join(script_dir, "exploraOSiconrounded.png"))
 home_image_photo = ctk.CTkImage(light_image=home_image_file, dark_image=home_image_file)
 home_image_label = ctk.CTkLabel(taskbar_home_frame, image=imagephoto, corner_radius=0, text="")
 home_image_label.pack(side="left")
 home_label_maintenance = ctk.CTkLabel(taskbar_home_frame, text="Soon!", font=Defaultfont)
 home_label_maintenance.pack(side="left")


 theme_btn = ctk.CTkButton(taskbar, corner_radius=0, command=switch_theme, width=28, text="Switch Theme")
 theme_btn.pack(side="left", fill="y")

 test_btn = ctk.CTkButton(taskbar, corner_radius=0, command=test_window, width=28, text="Test window")
 test_btn.pack(side="left", fill="y")

 settings_btn = ctk.CTkButton(taskbar, corner_radius=0, command=settings_window, width=28, text="Settings")
 settings_btn.pack(side="left", fill="y")

 expver_btn = ctk.CTkButton(taskbar, corner_radius=0, command=expver_window, width=28, text="Expver")
 expver_btn.pack(side="left", fill="y")

 notepad_btn = ctk.CTkButton(taskbar, corner_radius=0, command=notepad_window, width=28, text="Notepad")
 notepad_btn.pack(side="left", fill="y")


 
 try:
  if theme == "black":
   #window.configure(bg="#706486")
   desktop_content.configure(bg="#706486")
  
   ctk.set_appearance_mode("dark")
   taskbar.configure(bg="#7E7E7F")
   # btns colors
   
   theme_btn.configure(fg_color="#8D8D8E")
   theme_btn.configure(text_color="white")
   theme_btn.configure(hover_color="#828284")

   home_btn.configure(fg_color="#616060")
   home_btn.configure(text_color="white")
   home_btn.configure(hover_color="#828284")

   test_btn.configure(fg_color="#8D8D8E")
   test_btn.configure(text_color="white")
   test_btn.configure(hover_color="#828284")

   settings_btn.configure(fg_color="#8D8D8E")
   settings_btn.configure(text_color="white")
   settings_btn.configure(hover_color="#828284")

   expver_btn.configure(fg_color="#8D8D8E")
   expver_btn.configure(text_color="white")
   expver_btn.configure(hover_color="#828284")

   notepad_btn.configure(fg_color="#8D8D8E")
   notepad_btn.configure(text_color="white")
   notepad_btn.configure(hover_color="#828284")

   home_close_btn.configure(fg_color="#8D8D8E")
   home_close_btn.configure(text_color="white")
   home_close_btn.configure(hover_color="#828284")

   home_label_maintenance.configure(text_color="white")
   home_label_title.configure(text_color="white")
   
  

  elif theme == "white":
   #window.configure(bg="#D4C5F0")
   desktop_content.configure(bg="#D4C5F0")
  
   ctk.set_appearance_mode("white")
   taskbar.configure(bg="#F5F5F5")
   # btns colors
   
   theme_btn.configure(fg_color="white")
   theme_btn.configure(text_color="black")
   theme_btn.configure(hover_color="#F2F1F1")

   home_btn.configure(fg_color="#C6C6C6")
   home_btn.configure(text_color="black")
   home_btn.configure(hover_color="#F2F1F1")

   test_btn.configure(fg_color="white")
   test_btn.configure(text_color="black")
   test_btn.configure(hover_color="#F2F1F1")

   settings_btn.configure(fg_color="white")
   settings_btn.configure(text_color="black")
   settings_btn.configure(hover_color="#F2F1F1")

   expver_btn.configure(fg_color="white")
   expver_btn.configure(text_color="black")
   expver_btn.configure(hover_color="#F2F1F1")

   notepad_btn.configure(fg_color="white")
   notepad_btn.configure(text_color="black")
   notepad_btn.configure(hover_color="#F2F1F1")

   home_close_btn.configure(fg_color="white")
   home_close_btn.configure(text_color="black")
   home_close_btn.configure(hover_color="#F2F1F1")

   home_label_maintenance.configure(text_color="black")
   home_label_title.configure(text_color="black")
   
   
 except tk.TclError as e:
  window.configure(bg="#706486")
  desktop_content.destroy()
  desktop_content = tk.Frame(window, bg=window["bg"], name="desktop_content")
  desktop_content.pack(fill=tk.BOTH, expand=True)
  desktop_content.lift()
  reload_desktop("", "")



def reload_desktop(additional, framename):
  global desktop_content
  for childrens in desktop_content.winfo_children():
   childrens.destroy()
  load_desktop()
  if hasframeopen == True:
   create_frame(currentframename)
   

  

window = tk.Tk()
window.title("ExploraOS")
window.attributes("-fullscreen", True)
fullscreen = True
window.configure(bg="black")
window.iconbitmap(favicon)
window.geometry("989x739")


desktop_content = tk.Frame(window, bg=window["bg"], name="desktop_content")
desktop_content.pack(fill=tk.BOTH, expand=True)
desktop_content.lift()





thread = threading.Thread(target=boot) 
thread.start()

window.mainloop()
