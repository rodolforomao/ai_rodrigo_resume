import os
import time
import psutil
import subprocess
import pyautogui
import pygetwindow as gw


from selenium import webdriver

from selenium.common.exceptions import NoSuchWindowException, TimeoutException

_driver = None

def capturar_browser(chromeDriverPath = r"lib\chromedriver.exe", port = None):
    global _driver
    driver = None
    file_path = os.path.join(chromeDriverPath)
    if verificar_chrome_aberto() and os.path.exists(file_path):
        if _driver is None:
            caminho_chromedriver = chromeDriverPath
            porta_depuração = 5555

            comando_chrome = f'{caminho_chromedriver} --remote-debugging-port={porta_depuração}'
            subprocess.Popen(comando_chrome, shell=True)
            opcoes_chrome = webdriver.ChromeOptions()
            opcoes_chrome.debugger_address = f'127.0.0.1:{porta_depuração}'
            opcoes_chrome.add_argument("detach=True")
            opcoes_chrome.add_argument("--force-device-scale-factor=1")  # Set zoom level to 100%

            driver = webdriver.Chrome(options=opcoes_chrome)
            _driver = driver
        else:
            driver = check_window_and_switch(_driver)
    return driver

def check_window_and_switch(driver):
    try:
        # Perform a simple action to check if the window is still accessible
        driver.title
    except:
        # If there's an error, print a message and attempt to switch windows
        print("Current window is not accessible. Attempting to switch windows.")
        for handle in driver.window_handles:
            try:
                driver.switch_to.window(handle)
                driver.title  # Test if this window is accessible
                print(f"Switched to accessible window: {handle}")
                return driver
            except:
                continue
        # If no windows are accessible, raise an error or take an appropriate action
        print("No accessible windows found. Exiting.")
        driver.quit()
        raise Exception("No accessible windows found.")
    return driver

def checkUrl(url, chromeDriverPath = r"chromedriver.exe"):
    driver = capturar_browser()
    if driver is not None:
        url_atual = driver.current_url
        
        if url in url_atual:
            return True
        else:
            return False
    return None

def closeAllChromeInstances():
    loged = login_util.login(True, False)
    if loged:
        print('Já esta logado.')
        return
    subprocess.call("TASKKILL /f  /IM  CHROME.EXE")
    
    
def redirectToDatatableAnatelPage(address = None, chromeDriverPath = r"chromedriver.exe"):
    driver = capturar_browser()
    if driver is not None:
        try:
            if address is None:
                driver.get("https://apps.anatel.gov.br/acesso/PortalDeSistemas.aspx")
            else:
                driver.get(address)
            return True
        except NoSuchWindowException as e:
            print("Window not found error:", e)
            # Handle the error here, e.g., reopen the browser or log the error
    return False
    
def verificar_chrome_aberto():
    for proc in psutil.process_iter(['pid', 'name']):
        if 'chrome.exe' in proc.info['name']:
            return True
    print('Aguardando que o chrome seja aberto pelo usuário')
    return False

def verificar_chrome_aberto_timeout(intervaloSegundos=0.25, tentativas=4*10):
    for tentativa in range(tentativas):
        for proc in psutil.process_iter(['pid', 'name']):
            if 'chrome.exe' in proc.info['name']:
                return True
        time.sleep(intervaloSegundos)
    
    return False

def getTitleBrowser():
    listbrowser = gw.getWindowsWithTitle('Google Chrome')
    if len(listbrowser):
        chrome_window = gw.getWindowsWithTitle('Google Chrome')[0]
        return chrome_window.title
    return None