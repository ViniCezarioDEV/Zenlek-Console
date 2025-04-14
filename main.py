import subprocess
import os
import sys
import requests

try:
    from colorama import init, Fore, Style
except ImportError:
    print('[*] Colorama package is missing, downloding this package')
    subprocess.call([sys.executable, '-m', 'pip', 'install', 'colorama'])


#============version================
VERSION = 1.1
version_request = requests.get('https://github.com/vinicezariodev/zenlek-console/blob/main/version.json')


#============colorama styles================
init(autoreset=True)
#=====colors======
CYAN = Fore.CYAN
RED = Fore.RED
YELLOW = Fore.YELLOW
WHITE = Fore.WHITE
PURPLE = Fore.MAGENTA

LIGHTCYAN = Fore.LIGHTCYAN_EX + Style.BRIGHT
LIGHTWHITE = Fore.WHITE + Style.BRIGHT
LIGHTPURPLE = Fore.LIGHTMAGENTA_EX + Style.BRIGHT
LIGHTYELLOW = Fore.YELLOW + Style.BRIGHT
NORMAL = Style.NORMAL + Fore.WHITE



def CHECK_UPDATES():
    #search for updates using GITHUB request,
    #on github make a file with current version
    #on this code make a variable with current verion
    #if version of this code is below then github version, update the code
    #else nothing happen
    pass



def LOGO():
    print(f'''
   \t   {LIGHTCYAN}ZENLEK CONSOLE{NORMAL}{CYAN}
                                                        
   @@@@@@@@              @@@@@@@@   
          @@@@@@@@@@@@@@@@          
    @@@@         @@         @@@@    
       @@@@@            @@@@@       
           @@@@@@  @@@@@@           
            @@@@    @@@@            
         @@@@          @@@@         
      @@@@                @@@@      
       @@@@@            @@@@@       
           @@@@      @@@@@          
   @@@@       @@@  @@@       @@@@   
    @@@@@@@@            @@@@@@@@    
          @@@@@@    @@@@@@          
               @@@@@@   
                                                                     
    ''')

def INIT_INPUT():
    choice = input(f'{LIGHTWHITE} —$ {NORMAL}')

    if choice.lower() in ['help', 'commands', 'service', 'services']:
        print(f'''
    {LIGHTCYAN}AIDA{NORMAL} Music Downloader
    {LIGHTCYAN}PBM{NORMAL} Personal Backup Manager
    {LIGHTCYAN}PPM{NORMAL} Personal Password Manager
    {LIGHTCYAN}SSP{NORMAL} Show Personal Passwords''')



    """
    if choice.lower() == 'spot':
        try:
            subprocess.run(["spotdl", link, "--log-level", "NOTSET", "--format", "mp3", "--bitrate", "320k"],
                           check=True)
            print(f'{LIGHTCYAN}[+]{NORMAL}Download completed with Success')
        except FileNotFoundError as e:
            print(f'{LIGHTCYAN}[*]{NORMAL} SpotDL package is missing, downloding this package')
            subprocess.call([sys.executable, '-m', 'pip', 'install', 'spotdl'])
    """


#======startup======
LOGO()
while True:
    INIT_INPUT()
