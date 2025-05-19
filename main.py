import binascii
import subprocess
import sys
import os
import shutil
import zipfile
import urllib.request
import tarfile
import platform
import base64
import hashlib

if platform.system() == 'Windows':
    import winreg
try:
    from cryptography.fernet import Fernet
    from cryptography.fernet import InvalidToken
except ImportError:
    print('[*] cryptography package is missing, downloading this package')
    subprocess.call([sys.executable, '-m', 'pip', 'install', 'cryptography'])
    from cryptography.fernet import Fernet
    from cryptography.fernet import InvalidToken
try:
    from colorama import init, Fore, Style
except ImportError:
    print('[*] Colorama package is missing, downloading this package')
    subprocess.call([sys.executable, '-m', 'pip', 'install', 'colorama'])
    from colorama import init, Fore, Style
try:
    from youtube_search import YoutubeSearch
except ImportError:
    print('[*] youtube-search package is missing, downloading this package')
    subprocess.call([sys.executable, '-m', 'pip', 'install', 'youtube-search'])
    from youtube_search import YoutubeSearch
try:
    from yt_dlp import YoutubeDL
except ImportError:
    print('[*] yt-dlp package is missing, downloading this package')
    subprocess.call([sys.executable, '-m', 'pip', 'install', 'yt-dlp'])
    from yt_dlp import YoutubeDL
try:
    import requests
except ImportError:
    print('[*] requests package is missing, downloading this package')
    subprocess.call([sys.executable, '-m', 'pip', 'install', 'requests'])
    import requests
try:
    from pwinput import pwinput
except ImportError:
    print('[*] pwinput package is missing, downloading this package')
    subprocess.call([sys.executable, '-m', 'pip', 'install', 'pwinput'])
    from pwinput import pwinput


ffmpeg_installed = shutil.which("ffmpeg") is not None
if not ffmpeg_installed:
    system = platform.system().lower()

    if system == "windows":
        url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
        archive = "ffmpeg.zip"
    elif system == "linux":
        url = "https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-i686-static.tar.xz"
        archive = "ffmpeg.tar.xz"
    elif system == "darwin":  # macOS
        url = "https://evermeet.cx/ffmpeg/getrelease/zip"
        archive = "ffmpeg.zip"
    else:
        raise Exception(f"Unsupported OS: {system}")

    print(f"[*] Downloading FFmpeg for {system}...")
    urllib.request.urlretrieve(url, archive)

    extract_dir = os.path.join(os.getcwd(), "ffmpeg_bin")
    os.makedirs(extract_dir, exist_ok=True)

    print("[*] Extracting FFmpeg...")
    if archive.endswith(".zip"):
        with zipfile.ZipFile(archive, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
    elif archive.endswith(".tar.xz"):
        with tarfile.open(archive, "r:xz") as tar_ref:
            tar_ref.extractall(extract_dir)

    os.remove(archive)

    ffmpeg_path = None
    for root, dirs, files in os.walk(extract_dir):
        if system == "windows" and "ffmpeg.exe" in files:
            ffmpeg_path = root
        elif "ffmpeg" in files:
            ffmpeg_path = root

    if not ffmpeg_path:
        raise Exception("FFmpeg binary not found after extraction")

    print(f"[+] FFmpeg ready at: {ffmpeg_path}")

    if system == 'windows':
        try:
            current_path = os.environ.get('PATH', '')
            new_path = current_path + f";{ffmpeg_path}"

            os.environ['PATH'] = new_path

            reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Environment', 0, winreg.KEY_WRITE)
            winreg.SetValueEx(reg_key, 'Path', 0, winreg.REG_EXPAND_SZ, new_path)
            winreg.CloseKey(reg_key)

            print(f"[+] {ffmpeg_path} added to system PATH")
        except Exception as e:
            print(f"[-] Failed to add to PATH: {e}")

    elif system in ['linux', 'darwin']:
        try:
            config_file = os.path.expanduser('~/.bashrc') if system == 'linux' else os.path.expanduser('~/.zshrc')

            with open(config_file, 'a') as file:
                file.write(f'\n# Add FFmpeg to PATH\nexport PATH="{ffmpeg_path}:$PATH"\n')

            print(f"[+] {ffmpeg_path} added to system PATH")
        except Exception as e:
            print(f"[-] Failed to add to PATH: {e}")


#============ colorama styles ================
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


#============ version ================
LOCAL_VERSION = 1.06



#============ misc functions ============
def CLEAR_TERMINAL():
    if os.name == 'nt': #if are windows OS
        os.system('cls')
    else: #else are linux or mac OS
        os.system('clear')

def STRING_TO_KEY(password, salt=None):
    if salt is None:
        salt = os.urandom(16)
    hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
    fernet_key = base64.urlsafe_b64encode(hash)
    return fernet_key, salt

def ENCRYPT(content, key):
    fernet_key, salt = STRING_TO_KEY(key)
    fernet = Fernet(fernet_key)
    crypt_text = fernet.encrypt(content.encode())
    return base64.urlsafe_b64encode(salt + crypt_text).decode()

def DECRYPT(content, key):
    try:
        data = base64.urlsafe_b64decode(content.encode())
        if len(data) < 16:  # Salt mínimo de 16 bytes.
            raise ValueError("Encrypted data Invalid.")
        salt, crypt_text = data[:16], data[16:]
        fernet_key, _ = STRING_TO_KEY(key, salt)
        fernet = Fernet(fernet_key)
        return fernet.decrypt(crypt_text).decode()
    except (binascii.Error, ValueError) as e:
        print(f"Decrypt Error: {e}")
        return None

def PASSWORD():
    password = pwinput(mask='*', prompt='Password >>> ').strip()
    return password


#=========== features functions ============
def CHECK_UPDATES():
    version_request = requests.get('https://raw.githubusercontent.com/ViniCezarioDEV/Zenlek-Console/main/version.json')
    current_version = float(version_request.json()['version'])
    if LOCAL_VERSION < current_version:
        print(f'{LIGHTCYAN}[*]{NORMAL} New update detected, downloading new version')
        update_url = 'https://raw.githubusercontent.com/ViniCezarioDEV/Zenlek-Console/main/main.py'
        new_code = requests.get(update_url)

        if new_code.status_code == 200:
            with open('main.py', 'w', encoding='utf-8') as f:
                f.write(new_code.text)
            input(f'{GREEN}[+]{NORMAL} New version downloaded successfully\n\nRe-open the application')
            sys.exit()
        else:
            print(f'{RED}[-]{NORMAL} Error while downloading new version\n\nContinue using: {LOCAL_VERSION} version')

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

    elif choice.lower() == 'aida':
        AIDA_INIT()

    elif 'ssp' in choice:
        results = SSP(choice)
        if results:
            for item in results:
                print(item)

    elif choice.lower() == 'ppm':
        PPM()

    elif choice.lower() == 'clear':
        CLEAR_TERMINAL()
        LOGO()



#============= AIDA ==============
def AIDA_INIT():
    global aida_download_folder
    aida_download_folder = os.getcwd()
    AIDA_LOGO()
    AIDA_INPUT()

def AIDA_LOGO():
    global aida_download_folder
    CLEAR_TERMINAL()
    print(f'''{LIGHTYELLOW}
    ░█████╗░██╗██████╗░░█████╗░
    ██╔══██╗██║██╔══██╗██╔══██╗
    ███████║██║██║░░██║███████║
    ██╔══██║██║██║░░██║██╔══██║
    ██║░░██║██║██████╔╝██║░░██║
    ╚═╝░░╚═╝╚═╝╚═════╝░╚═╝░░╚═╝{NORMAL}

    {YELLOW}Download folder: {NORMAL}{aida_download_folder}''')

def AIDA_INPUT():
    while True:

        try:
            choice = int(input(f'''
    {LIGHTYELLOW}[1]{NORMAL} Youtube mp3
    {LIGHTYELLOW}[2]{NORMAL} Youtube mp4
    {LIGHTYELLOW}[3]{NORMAL} Spotify mp3
    {LIGHTYELLOW}[4]{NORMAL} Change download folder
    {LIGHTYELLOW}[5]{NORMAL} Back to main menu

    {LIGHTYELLOW}[AIDA]{NORMAL}{LIGHTWHITE} >>>{NORMAL}  '''))
        except ValueError:
            print(f'{LIGHTYELLOW}[AIDA]{NORMAL} Invalid Option')
            continue


        if choice == 1: #yt mp3
            AIDA_YOUTUBE_MP3()
        elif choice == 2: #yt mp4
            AIDA_YOUTUBE_MP4()
        elif choice == 3: #spotify
            DOWNLOAD_AIDA_SPOTFY()
        elif choice == 4: #change download folder
            AIDA_CHANGE_FOLDER()
            continue
        elif choice == 5: #back to main menu
            break
        else:
            print(f'{LIGHTYELLOW}[AIDA]{NORMAL} Invalid Option')

    CLEAR_TERMINAL()
    LOGO()
    INIT_INPUT()

def AIDA_YOUTUBE_MP3():
    aida_mp3_list = []
    while True:
        choice = input(f'    {LIGHTYELLOW}[AIDA-mp3]{NORMAL} {LIGHTCYAN}Music name{WHITE}{NORMAL}/{CYAN}Youtube Link{WHITE}/{LIGHTCYAN}"d" for download{NORMAL}{WHITE} >>> ')

        if choice.lower() == 'd': #start download
            if aida_mp3_list:
                break #go to DOWNLOAD_AIDA_YOUTUBE_MP3()
            else:
                print(f"\n    {LIGHTYELLOW}[AIDA-mp3]{NORMAL} Mp3 list is empty")

        else:
            aida_mp3_list.append(choice)

    DOWNLOAD_AIDA_YOUTUBE_MP3(aida_mp3_list)

def DOWNLOAD_AIDA_YOUTUBE_MP3(music_list):
    global aida_download_folder
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(aida_download_folder, '%(title)s.%(ext)s'),
        'quiet': True,
        'no_warnings': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
    }

    for music in music_list:
        if not 'https' in music:
            results = YoutubeSearch(music, max_results=1).to_dict()
            music = 'https://www.youtube.com' + results[0]['url_suffix']

        try:
            with YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(music, download=True)
                title = info_dict.get('title', 'title unknown')
                print(f'{GREEN}[+] Downloaded{NORMAL} {title}')

        except Exception as e:
            print(f'{RED}[-] Failure ({e}){NORMAL} {music}')

def AIDA_YOUTUBE_MP4():
    aida_mp4_list = []
    while True:
        choice = input(f'    {LIGHTYELLOW}[AIDA-mp4]{NORMAL} {LIGHTCYAN}Youtube Link{WHITE}{NORMAL}/{CYAN}"d" for download{WHITE} >>> ')

        if choice.lower() == 'd': #start download
            if aida_mp4_list:
                break #go to DOWNLOAD_AIDA_YOUTUBE_MP3()
            else:
                print(f"\n    {LIGHTYELLOW}[AIDA-mp4]{NORMAL} Mp4 list is empty")

        elif 'youtube.com/watch' in choice or 'youtu.be/' in choice:
            aida_mp4_list.append(choice)

        else:
            print(f"\n    {LIGHTYELLOW}[AIDA-mp4]{NORMAL} Must to be Youtube link (https://youtube.com/watch....)")

    DOWNLOAD_AIDA_YOUTUBE_MP4(aida_mp4_list)

def DOWNLOAD_AIDA_YOUTUBE_MP4(video_list):
    global aida_download_folder
    ydl_opts = {
        'format': 'bv*+ba/best',
        'merge_output_format': 'mp4',
        'outtmpl': f"{aida_download_folder}/%(title)s.%(ext)s",
        'quiet': True,
        'no_warnings': True,
    }

    for video in video_list:
        try:
            with YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(video, download=True)
                title = info_dict.get('title', 'title unknown')
                print(f'{GREEN}[+] Downloaded{NORMAL} {title}')

        except Exception as e:
            print(f'{RED}[-] Failure ({e}){NORMAL} {video}')

def DOWNLOAD_AIDA_SPOTFY():
    spotdl_installed = shutil.which("spotdl") is not None
    if not spotdl_installed:
        print(f'{LIGHTCYAN}[*]{NORMAL} SpotDL package is missing, installing it...')
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'spotdl'])
            print(f'{LIGHTCYAN}[+]{NORMAL} SpotDL successfully installed')
        except subprocess.CalledProcessError as e:
            print(f'{LIGHTCYAN}[-]{NORMAL} Failed to install SpotDL: {e}')
            return

    while True:
        link = input(f'    {LIGHTYELLOW}[AIDA-spotify]{NORMAL} {LIGHTCYAN}Spotify Link (playlist/music){WHITE}{NORMAL} >>> ')
        if 'open.spotify.com' in link:
            break
        else:
            print(f"{LIGHTYELLOW}[*]{NORMAL} Invalid link, please enter a valid Spotify link.")

    try:
        subprocess.run(["spotdl", "download", link, "--log-level", "NOTSET", "--format", "mp3", "--bitrate", "320k", "--output", f"{aida_download_folder}",],
                       check=True)
        print(f'{LIGHTCYAN}[+]{NORMAL} Download completed successfully')

    except subprocess.CalledProcessError as e:
        print(f'{LIGHTCYAN}[-]{NORMAL} Error during download: {e}')
    except Exception as e:
        print(f'{LIGHTCYAN}[-]{NORMAL} Unexpected error: {e}')

def AIDA_CHANGE_FOLDER():
    global aida_download_folder
    while True:
        new_folder = input(f'{LIGHTYELLOW}[AIDA]{NORMAL} New folder path >>> ')
        if os.path.isdir(new_folder):
            aida_download_folder = new_folder
            break
    AIDA_LOGO()
    AIDA_INPUT()


def SSP(fulltext):
    try:
        if not os.path.exists('ppl.txt'):
            with open('ppl.txt', 'w', encoding='utf-8') as f:
                return []

        with open('ppl.txt', 'r', encoding='utf-8') as f:
            encrypted_lines = []
            seen = set()
            for line in f:
                line = line.strip()
                if line and line not in seen:
                    seen.add(line)
                    encrypted_lines.append(line)

        commands = fulltext.split(' ')[1:]
        if not commands:
            return []

        password = PASSWORD()
        if not password:
            return []

        approved_services = []
        seen_decrypted = set()

        for encrypted in encrypted_lines:
            try:
                decrypted = DECRYPT(encrypted, password)
                if decrypted and decrypted not in seen_decrypted:
                    if all(cmd in decrypted for cmd in commands):
                        approved_services.append(decrypted)
                        seen_decrypted.add(decrypted)
            except:
                continue

        return approved_services

    except:
        return []


def PPM():
    CLEAR_TERMINAL()
    print('''
       ___  ___  __ _ 
      / _ \/ _ \/  ' \\
     / .__/ .__/_/_/_/
    /_/  /_/              
                                ''')

    print('''
    [1] Add a new service
    [2] Patch a service
    [3] Delete a service
    [4] Exit
    ''')

    while True:
        choice = int(input('[PPM] Select an option >>> '))

        match choice:
            case 1:
                PPM_ADD()
            case 2:
                PPM_PATCH()
            case 3:
                PPM_DELETE()
            case 4:
                input('[PPM] Bye. Press Enter to back')
                break
            case _:
                print('[PPM] Invalid option')
    CLEAR_TERMINAL()
    LOGO()
    INIT_INPUT()

def PPM_ADD():
    try:
        text_parts = []
        print('[PPM(add)] Type 99 to add')

        while True:
            desc = input('[PPM(add)] Description >>> ').strip()
            if desc == '99':
                break

            value = input('[PPM(add)] Value >>> ').strip()
            if not desc or not value:
                print("Description and value cannot be empty")
                continue

            text_parts.append(f"{desc}:{value}|")

        if not text_parts:
            input('[PPM] No service added. Press Enter to back')
            return
        text = ''.join(text_parts)[:-1]

        password = PASSWORD()
        if not password:
            return

        encrypted_text = ENCRYPT(text, password)
        if not encrypted_text:
            input('[PPM] Failed to encrypt. Press Enter to back')
            return

        with open('ppl.txt', 'a', encoding='utf-8') as file:
            file.write(encrypted_text + '\n')

        input('[PPM] Service added. Press Enter to back')

    except Exception as e:
        print(f"PPM_ADD Error: {e}")
        input('[PPM] Operation failed. Press Enter to back')

def PPM_PATCH():
    try:
        password = PASSWORD()
        if not password:
            return

        with open('ppl.txt', 'r', encoding='utf-8') as file:
            lines = [line.strip() for line in file.readlines() if line.strip()]

        decrypted_lines = []
        for line in lines:
            decrypted = DECRYPT(line, password)
            if decrypted:
                decrypted_lines.append(decrypted)
            else:
                print(f"Failed to decrypt line: {line[:20]}")
                return

        print('All Services')
        for i, line in enumerate(decrypted_lines):
            parts = line.split('|')
            if len(parts) >= 2:
                print(f'[{i + 1}] {parts[0]} | {parts[1]}')
            else:
                print(f'[{i + 1}] Invalid format: {line[:20]}')

        try:
            choice = int(input('\n[PPM] Which service want to change? ')) - 1
            if choice < 0 or choice >= len(lines):
                print("Invalid selection")
                return
        except ValueError:
            print("Please enter a valid number")
            return

        print('[PPM] Type 99 to finish')
        new_parts = []
        while True:
            desc = input('[PPM(modify)] New description: ').strip()
            if desc == '99':
                break
            value = input('[PPM(modify)] New value: ').strip()
            if not desc or not value:
                print("Description and value cannot be empty")
                continue
            new_parts.append(f"{desc}:{value}")

        if not new_parts:
            print("No changes made")
            return

        new_text = "|".join(new_parts)
        encrypted_text = ENCRYPT(new_text, password)
        if not encrypted_text:
            print("Failed to encrypt new entry")
            return

        lines[choice] = encrypted_text + '\n'
        with open('ppl.txt', 'w', encoding='utf-8') as file:
            file.writelines(lines)

        input('[PPM] Service modified. Press Enter to back')

    except Exception as e:
        print(f"Error: {e}")
        input('[PPM] Operation failed. Press Enter to back')

def PPM_DELETE():
    try:
        password = PASSWORD()
        if not password:
            return

        with open('ppl.txt', 'r', encoding='utf-8') as file:
            lines = [line.strip() for line in file.readlines() if line.strip()]

        decrypted_lines = []
        for line in lines:
            decrypted = DECRYPT(line, password)
            if decrypted:
                decrypted_lines.append(decrypted)
            else:
                print(f"Failed to decrypt line: {line[:20]}")
                return

        print('All Services')
        for i, line in enumerate(decrypted_lines):
            parts = line.split('|')
            if len(parts) >= 2:
                print(f'[{i + 1}] {parts[0]} | {parts[1]}')
            else:
                print(f'[{i + 1}] Invalid format: {line[:20]}')

        try:
            choice = int(input('\n[PPM] Which service want to delete? ')) - 1
            if choice < 0 or choice >= len(lines):
                print("Invalid selection")
                return
        except ValueError:
            print("Please enter a valid number")
            return

        lines.pop(choice)
        with open('ppl.txt', 'w', encoding='utf-8') as file:
            file.writelines([line + '\n' for line in lines])

        input('[PPM] Service deleted. Press Enter to back')

    except Exception as e:
        print(f"Error: {e}")
        input('[PPM] Operation failed. Press Enter to back')






#======startup======
CLEAR_TERMINAL()
LOGO()
CHECK_UPDATES()
while True:
    INIT_INPUT()
