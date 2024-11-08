import os

def encontrar_chrome():
    try:
        import winreg
        reg_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe"
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path) as key:
            chrome_path = winreg.QueryValue(key, None)
            return chrome_path
    except Exception as e:
        print(f"Erro ao encontrar o Chrome: {e}")
        return None

def get_datauser_chrome():
    # chrome://version/
    return os.path.join(os.path.expanduser("~"), 'AppData', 'Local', 'Google', 'Chrome', 'User Data')  # For Windows

def get_datauser_chrome_dev():
    # chrome://version/
    return os.path.join(os.path.expanduser("~"), 'AppData', 'Local', 'Google', 'Chrome Dev', 'User Data')  # For Windows

def encontrar_chrome_dev():
    try:
        import winreg
        reg_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe"  # Caminho do Chrome Dev
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path) as key:
            chrome_dev_path = winreg.QueryValue(key, None)
            return chrome_dev_path
    except Exception as e:
        print(f"Erro ao encontrar o Chrome Dev: {e}")
        return None
    
def get_profile_and_set_user_chrome_dev(name):    
    profiles = get_profile_chrome_dev(get_datauser_chrome_dev(), True)
    
    if len(profiles) > 1:
        for profile in profiles:
            if name in profile:
                return profile
    
    for profile in profiles:
        return profile
    
def get_profile_chrome_dev(profile_dir, debug = False):
    profiles = [d for d in os.listdir(profile_dir) if os.path.isdir(os.path.join(profile_dir, d)) and d.startswith("Profile")]

    # Print available profiles
    if debug:
        print("Available Profiles:")
        for profile in profiles:
            print(profile)
        
    return profiles