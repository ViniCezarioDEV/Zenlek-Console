import subprocess
import os
import sys
import requests
try:
    from colorama import init, Fore, Style
except ImportError:
    print('[*] Colorama package is missing, downloding this package')
    subprocess.call([sys.executable, '-m', 'pip', 'install', 'colorama'])


#============colorama styles================
init(autoreset=True)
#=====colors======
CYAN = Fore.CYAN
RED = Fore.RED
YELLOW = Fore.YELLOW
WHITE = Fore.WHITE
PURPLE = Fore.MAGENTA
GREEN = Fore.GREEN

LIGHTCYAN = Fore.LIGHTCYAN_EX + Style.BRIGHT
LIGHTWHITE = Fore.WHITE + Style.BRIGHT
LIGHTPURPLE = Fore.LIGHTMAGENTA_EX + Style.BRIGHT
LIGHTYELLOW = Fore.YELLOW + Style.BRIGHT
NORMAL = Style.NORMAL + Fore.WHITE


#============version================
LOCAL_VERSION = 1.1




def CHECK_UPDATES():
    version_request = requests.get('https://raw.githubusercontent.com/ViniCezarioDEV/Zenlek-Console/main/version.json')
    CURRENT_VERSION = float(version_request.json()['version'])
    if LOCAL_VERSION < CURRENT_VERSION:
        print(f'{LIGHTCYAN}[*]{NORMAL} New update detected, downloading new version')
        update_url = 'https://raw.githubusercontent.com/ViniCezarioDEV/Zenlek-Console/main/main.py'
        new_code = requests.get(update_url)

        if new_code.status_code == 200:
            with open('main.py', 'w', encoding='utf-8') as f:
                f.write(new_code.text)
            input(f'{GREEN}[+]{NORMAL} New version downloaded successfully\n\nRe-open the application')
            sys.exit()
        else:
            print(f'{RED}[-]{NORMAL} Error while downloding new version\n\nContinue using: {LOCAL_VERSION} version')



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
CHECK_UPDATES()
while True:
    INIT_INPUT()
