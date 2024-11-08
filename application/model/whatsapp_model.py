import os
import re
import json
import time
import psutil

import subprocess
import urllib.parse
from datetime import datetime

from util.files_util import Files

import unicodedata

import threading

import util.chrome_util as chrome
import util.elements_util as elements

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.action_chains import ActionChains

from selenium.common.exceptions import WebDriverException

import speech_recognition as sr
#from pydub import AudioSegment
import soundfile as sf
import speech_recognition as sr
import os

from util.files_util import Files
from util.string_util import StringUtil
from util.whatsapp_util import WhatsappUtils

from application.config.config import WHATSAPP_GROUPS

class WhatsappModel:
    
    _driver = None
    stop_thread = False
    
    def __init__(self):
        print(f'Class: {self.__class__.__name__} - constructor')

    def lerMensagensWhatsapp(self):
        driver = self.capturar_browser_dev()
        if driver is None:
            driver = self.open_webbrowser(False)
        driver, perguntas = self.read_messages_groups(driver)
        return driver, perguntas
    
    def refresh_webdriver(self):
        try:
            driver = self.capturar_browser_dev()
            if driver is not None:
                driver.refresh()
        except Exception as e:
            print('Failed to refresh webdriver')
    
    def enviarMensagensWhatsapp(self, perguntas, respostas, driver = None):
        driver = self.capturar_browser_dev()
        if driver is None:
            driver = self.open_webbrowser(False)
        self.send_messages_groups(driver, perguntas, respostas)
        
        
    def display_users(self):
        users = self.model.get_all_users()
        self.view.show_users(users)

    def send_messages_groups(self, driver, perguntas, respostas):
        
        for pergunta in perguntas:
            group_name = pergunta['user_name']
            numero_to_send = pergunta['number']
            
        if respostas:
            if 'nova versão do ChatGPT' in respostas:
                return driver, None            
        
        mensagem_to_send = urllib.parse.quote(respostas)
        
        url = f"https://web.whatsapp.com/"
        driver.get(url)
        
        if elements.wait_for_element_to_load(driver,'wf-loading', elements.TYPE_FIND_BY_CLASS):
            try:
                element_addr = f"//div[@role='listitem']//span[@title='{group_name}']"
                element = elements.wait_for_element_to_load(driver,element_addr, elements.TYPE_FIND_BY_XPATH)
                if element:
                    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:00')
                    element.click()
                    element_addr = "//*[@aria-placeholder='Type a message' or @aria-placeholder='Digite uma mensagem']"
                    element = elements.wait_for_element_to_load(driver,element_addr, elements.TYPE_FIND_BY_XPATH)
                    if element:
                        element.send_keys(respostas)
                        element.send_keys(Keys.ENTER)
                        print(f"Mensagem enviada para {numero_to_send}")
                                                
                        start_time = time.time()
                        max_wait_time = 10  # segundos

                        mensagem_enviada = False
                        while time.time() - start_time < max_wait_time:
                            mensagens_enviadas = driver.find_elements(By.XPATH, "//div[@class='copyable-text']")
                            
                            for msg in mensagens_enviadas:
                                if mensagem_to_send in msg.text:
                                    data_hora = msg.get_attribute("data-pre-plain-text")
                                    data_hora_str = data_hora.split(']')[0][1:]  # Remove o "[" e obtém a parte da data
                                    try:
                                        data_hora_formatada = datetime.strptime(data_hora_str, '%H:%M, %d/%m/%Y')
                                    except Exception as e:
                                        try:
                                            data_hora_formatada = datetime.strptime(data_hora_str, '%H:%M, %m/%d/%Y')
                                        except Exception as e:
                                            print(e)

                                    # Compara as datas
                                    if data_hora_formatada.strftime('%Y-%m-%d %H:%M:%S') == timestamp:
                                        print(f"Mensagem enviada para {numero_to_send} às {data_hora}")
                                        if mensagem_to_send == mensagem_to_send:
                                            mensagem_enviada = True
                                            print(f"Mensagem conferida {numero_to_send}")
                                            
                                            english = True
                                            while True:
                                                
                                                # Verifica se está escrito "pending" - ou simbolo de pendente de envio, caso feche o browser com este simbolo, a mensagem normalmente não é enviada.
                                                if english:
                                                    status = ' Pending '
                                                else:
                                                    status = ' Pendente '
                                                    
                                                pending_status = driver.find_elements(By.XPATH, "//span[@aria-label='"+ status +"']")
                                                if pending_status:
                                                    print(f"Mensagem para {numero_to_send} ainda está pendente.")
                                                    time.sleep(0.25)
                                                    continue 
                                                
                                                element_msg_status = elements.wait_for_class_to_load(driver,"//span[@data-icon='msg-dblcheck']", elements.TYPE_FIND_BY_XPATH, True)
                                                aria_label = element_msg_status.get_attribute("aria-label")
                                                
                                                if 'Read' in aria_label or 'Lido' in aria_label:
                                                    break
                                                
                                                if 'Delivered' in aria_label or 'Entregue' in aria_label:
                                                    # SVG double check
                                                    svg_inside_message = driver.execute_script("""
                                                                var svg = document.querySelector("span[data-icon='msg-dblcheck'] svg");
                                                                return svg ? svg.outerHTML : null;
                                                            """)
                                                    svgExpected = '<svg viewBox="0 0 16 11" height="11" width="16" preserveAspectRatio="xMidYMid meet" class="" fill="none"><title>msg-dblcheck</title><path d="M11.0714 0.652832C10.991 0.585124 10.8894 0.55127 10.7667 0.55127C10.6186 0.55127 10.4916 0.610514 10.3858 0.729004L4.19688 8.36523L1.79112 6.09277C1.7488 6.04622 1.69802 6.01025 1.63877 5.98486C1.57953 5.95947 1.51817 5.94678 1.45469 5.94678C1.32351 5.94678 1.20925 5.99544 1.11192 6.09277L0.800883 6.40381C0.707784 6.49268 0.661235 6.60482 0.661235 6.74023C0.661235 6.87565 0.707784 6.98991 0.800883 7.08301L3.79698 10.0791C3.94509 10.2145 4.11224 10.2822 4.29844 10.2822C4.40424 10.2822 4.5058 10.259 4.60313 10.2124C4.70046 10.1659 4.78086 10.1003 4.84434 10.0156L11.4903 1.59863C11.5623 1.5013 11.5982 1.40186 11.5982 1.30029C11.5982 1.14372 11.5348 1.01888 11.4078 0.925781L11.0714 0.652832ZM8.6212 8.32715C8.43077 8.20866 8.2488 8.09017 8.0753 7.97168C7.99489 7.89128 7.8891 7.85107 7.75791 7.85107C7.6098 7.85107 7.4892 7.90397 7.3961 8.00977L7.10411 8.33984C7.01947 8.43717 6.97715 8.54508 6.97715 8.66357C6.97715 8.79476 7.0237 8.90902 7.1168 9.00635L8.1959 10.0791C8.33132 10.2145 8.49636 10.2822 8.69102 10.2822C8.79681 10.2822 8.89838 10.259 8.99571 10.2124C9.09304 10.1659 9.17556 10.1003 9.24327 10.0156L15.8639 1.62402C15.9358 1.53939 15.9718 1.43994 15.9718 1.32568C15.9718 1.1818 15.9125 1.05697 15.794 0.951172L15.4386 0.678223C15.3582 0.610514 15.2587 0.57666 15.1402 0.57666C14.9964 0.57666 14.8715 0.635905 14.7657 0.754395L8.6212 8.32715Z" fill="currentColor"></path></svg>';
                                                    if svg_inside_message == svgExpected:
                                                        break
                                                print(aria_label)
                                        break

                            if mensagem_enviada:
                                break
                        
                    else:
                        print(f"Erro ao enviar para {numero_to_send}: {e}")
            except Exception as e:
                print(f"Erro ao enviar para {numero_to_send}: {e}")
                
            
            
                
        return driver, perguntas

    def read_messages_groups(self, driver):
        driver.get('https://web.whatsapp.com')
        
        perguntas = []
        
        contador = 0
        index_group = 0
        while len(perguntas) == 0:
            element = elements.wait_for_element_to_load(driver,'wf-loading', elements.TYPE_FIND_BY_CLASS)
            if element:
                
                if len(WHATSAPP_GROUPS) <= index_group:
                    index_group = 0
                    time.sleep(90)
                group_name = WHATSAPP_GROUPS[index_group]
                index_group += 1
                
                element_addr = f"//div[@role='listitem']//span[@title='{group_name}']"
                try:
                    group_selected = elements.wait_for_element_to_load(driver,element_addr, elements.TYPE_FIND_BY_XPATH, True, True, False, timeout=5, poll_frequency=0.25, error_print = False)
                except Exception as e:
                    print('')
                    
                #list_unread_conversations = elements.wait_for_element_to_load(driver, element_addr, elements.TYPE_FIND_BY_XPATH, True, True)
                if group_selected:
                    for item in group_selected:
                        if item.is_enabled():
                            # parent_level_1 = elements.wait_for_element_to_load(item,self.get_recursive_level(), elements.TYPE_FIND_BY_XPATH, True)
                            # parent_level_2 = elements.wait_for_element_to_load(unread_item,self.get_recursive_level(2), elements.TYPE_FIND_BY_XPATH, True)
                            # parent_level_3 = elements.wait_for_element_to_load(unread_item,self.get_recursive_level(3), elements.TYPE_FIND_BY_XPATH, True)
                            # parent_level_6 = elements.wait_for_element_to_load(unread_item,self.get_recursive_level(6), elements.TYPE_FIND_BY_XPATH, True)
                            # parent_level_7 = elements.wait_for_element_to_load(unread_item,self.get_recursive_level(7), elements.TYPE_FIND_BY_XPATH, True)
                            # parent_level_8 = elements.wait_for_element_to_load(unread_item,self.get_recursive_level(8), elements.TYPE_FIND_BY_XPATH, True)
                            # parent_level_9 = elements.wait_for_element_to_load(unread_item,self.get_recursive_level(9), elements.TYPE_FIND_BY_XPATH, True)
                            # parent_level_10 = elements.wait_for_element_to_load(unread_item,self.get_recursive_level(10), elements.TYPE_FIND_BY_XPATH, True)
                            # parent_level_11 = elements.wait_for_element_to_load(unread_item,self.get_recursive_level(11), elements.TYPE_FIND_BY_XPATH, True)
                            
                            item_message = elements.wait_for_element_to_load(item,self.get_recursive_level(4), elements.TYPE_FIND_BY_XPATH, True)
                            user_name = elements.wait_for_element_to_load(item,self.get_recursive_level(5), elements.TYPE_FIND_BY_XPATH, True)
                            
                            user_name = user_name.text.split('\n')[0]
                            mensagem = item_message.text
                            print(mensagem)
                            is_audio_foward = False
                            is_audio = False
                            stringUtil = StringUtil()
                            if stringUtil.normalize(mensagem).startswith(stringUtil.normalize("Áudio")):
                                is_audio_foward = True
                            
                            if item_message.is_enabled():
                                try:
                                    item_message.click()
                                    print('Clicar para marcar como lido')
                                except Exception as e:
                                    pass

                            element_addr = '//div[@role="row"]/div[starts-with(@data-id, "false_")]'
                            element = elements.wait_for_element_to_load(driver,element_addr, elements.TYPE_FIND_BY_XPATH, True)
                            pattern = re.compile(r'false_(\d+)@')
                            cellphone_number = element.get_attribute('data-id')
                            is_user = True
                            if cellphone_number:
                                match = pattern.search(cellphone_number)
                                if match:
                                    cellphone_number = match.group(1)
                                    print("Número encontrado:", cellphone_number)
                                else:
                                    cellphone_number = re.search(r'false_(\d+-\d+)@g\.us', cellphone_number)
                                    cellphone_number = cellphone_number.group(1)
                                    is_user = False

                                whatspputil = WhatsappUtils()
                                if whatspputil.message_exists(mensagem,cellphone_number):
                                    print('Mensagem já processada')
                                    continue
                                
                                if is_audio_foward is False:
                                    is_audio = self.is_audio_duration(mensagem)
                                if is_audio or is_audio_foward:
                                    element_addr = "_amlr"
                                    element_list = elements.wait_for_element_to_load(driver,element_addr, elements.TYPE_FIND_BY_CLASS, True, True)
                                    file_audio = None
                                    if element_list:
                                        last_element = element_list[-1]
                                        file_audio = self.download_audio(driver, last_element)
                                    if file_audio is not None and file_audio is not False:
                                        to_path = f"{cellphone_number}_{user_name}"
                                        to_path = re.sub(r'[^\w\s]', '_', to_path)  # Replace non-word characters with underscore
                                        to_path = re.sub(r'\s+', '_', to_path)  # Replace whitespace (spaces, tabs) with underscore
                                        to_path = self.remove_accents(to_path.lower())
                                        mensagem = self.convert_audio_to_text(file_audio, to_path)
                                else:
                                    mensagem = re.sub(r'\d+$', '', mensagem).strip()
                                
                                # parent_level_5 = elements.wait_for_element_to_load(element,self.get_recursive_level(5), elements.TYPE_FIND_BY_XPATH, True)
                                # parent_level_6 = elements.wait_for_element_to_load(element,self.get_recursive_level(6), elements.TYPE_FIND_BY_XPATH, True)
                                toda_mensagem_da_conversa = elements.wait_for_element_to_load(element,self.get_recursive_level(7), elements.TYPE_FIND_BY_XPATH, True)
                                if toda_mensagem_da_conversa:
                                    
                                    #mensagem = whatspputil.get_conversation_and_save(toda_mensagem_da_conversa.text, cellphone_number)
                                    mensagem = whatspputil.get_msg_like_text(toda_mensagem_da_conversa.text, cellphone_number)
                                    
                                #mensagens_da_tela = elements.wait_for_element_to_load(element,self.get_recursive_level(8), elements.TYPE_FIND_BY_XPATH, True)
                                pass
                                    
                                perguntas.append({
                                    'number': cellphone_number,
                                    'user_name': user_name,
                                    'message': mensagem,
                                })
                                
                                
            if contador > 0:
                time.sleep(1)
            contador += 1
            if contador >= 5:
                return None, None
                
        return driver, perguntas

    def check_is_typing(self, driver):
        element_addr = "//span[@title='digitando...']"
        try:
            list_typing = elements.wait_for_element_to_load(driver,element_addr, elements.TYPE_FIND_BY_XPATH, True, True, False, timeout=5, poll_frequency=0.25, error_print = False)
        except Exception as e:
            print('')
        if list_typing:
            return True
        return False  # Retorne True se o elemento foi encontrado, caso contrário False

    def wait_user_typing(self, driver, timeout = 30):
        print(f"O usuário mandou uma mensagem, iremos aguardar {timeout} segundos, caso ele esteja digitando, zeramos o tempo de espera.")
        tempo_maximo = timeout
        ultimo_tempo = time.time()

        while True:
            if time.time() - ultimo_tempo > tempo_maximo:
                print("Tempo de espera finalizado!")
                break
            
            if self.check_is_typing(driver):
                time.sleep(3)
                print("O usuário está digitando, aguardando o tempo de espera padrão de " + str(timeout) + " segundos.")
                ultimo_tempo = time.time()  # Reseta o tempo

    def get_recursive_level(self, level = 1):
        return '.' + ('/..' * level)
    
    def remove_accents(self, input_str):
        # Normalize the string to decompose characters into base characters and accents
        normalized_str = unicodedata.normalize('NFD', input_str)
        # Filter out the accents by keeping only the base characters
        return ''.join(c for c in normalized_str if unicodedata.category(c) != 'Mn')

    def open_webbrowser(self, hidden = True):
        chrome_user_data_dir = chrome.get_datauser_chrome_dev()
        chrome_options = Options()
        if hidden:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument(f"user-data-dir={chrome_user_data_dir}")
        chrome_options.add_argument("profile-directory=Default")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--remote-debugging-port=9222")
        chrome_options.add_argument("--disable-gpu")
        return webdriver.Chrome(options=chrome_options)
        
    def is_audio_duration(self, item_message):
        match = re.match(r"^(?:\d{1,2}:)?\d{1,2}:\d{2}", item_message.strip())
        return bool(match)
    
    def convert_audio_to_text(self, file_audio, to_path): 
        resposta_audio = None
        recognizer = sr.Recognizer()

        file_name = os.path.basename(file_audio)
        if os.path.exists(file_audio):
            file = Files()
            file.ensure_directory_exists(f"files/{to_path}/")
            wav_file_path = f"files/{to_path}/{file_name}.wav"

            # Convert the .ogg file to .wav without using external executables
            data, samplerate = sf.read(file_audio)
            sf.write(wav_file_path, data, samplerate)

            # Load the .wav file for recognition
            with sr.AudioFile(wav_file_path) as source:
                audio_data = recognizer.record(source)

            try:
                resposta_audio = recognizer.recognize_google(audio_data, language="pt-BR")
                print("Recognized text:", resposta_audio)
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand the audio.")
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service; {e}")
                
        return resposta_audio
        
    def start_chrome_driver(self, chrome_options, result):
        try:
            result["driver"] = webdriver.Chrome(options=chrome_options)
        except WebDriverException as e:
            result["error"] = e


    def capturar_browser_dev(self, port=9222, timeout=3):
        driver = None
        try:
            base_path = os.path.dirname(os.path.abspath(__file__))
            file_path_1 = os.path.join(base_path, "lib", "chrome.exe")
            caminho_chromedriver = r"lib\chromedriver.exe"
            file_path_2 = os.path.join(caminho_chromedriver)
            if self.verificar_chrome_aberto() is False:
                driver = None
                self.driver = None
            if self.verificar_chrome_aberto() and (os.path.exists(file_path_1) or os.path.exists(file_path_2)):
                if self._driver is None:
                    porta_depuração = port
                    comando_chrome = f'{caminho_chromedriver} --remote-debugging-port={porta_depuração}'
                    subprocess.Popen(comando_chrome, shell=True)

                    opcoes_chrome = webdriver.ChromeOptions()
                    opcoes_chrome.debugger_address = f'127.0.0.1:{porta_depuração}'
                    opcoes_chrome.add_argument("detach=True")
                    opcoes_chrome.add_argument("--force-device-scale-factor=1")  # Set zoom level to 100%

                    # Dictionary to store the driver or error from the thread
                    result = {}
                    # Start the driver in a separate thread
                    driver_thread = threading.Thread(target=self.start_chrome_driver, args=(opcoes_chrome, result))
                    driver_thread.start()
                    driver_thread.join(timeout)  # Wait for the thread to finish or timeout

                    # Check if the driver was initialized successfully within the timeout
                    if "driver" in result:
                        driver = result["driver"]
                        self._driver = driver
                    else:
                        # Terminate thread if timeout reached and driver wasn't initialized
                        print("Timeout reached: Failed to initialize Chrome driver within the specified time.")
                        #driver_thread.join()  # Ensure thread is fully closed
                else:
                    driver = self._driver
                    driver.title
        except Exception as e:
            try:
                if self._driver:
                    self._driver.quit()
            except Exception as e:
                print(e)
            print(e)
            driver = None
            self.driver = None
        return driver
    
    def verificar_chrome_aberto(self):
        for proc in psutil.process_iter(['pid', 'name']):
            if 'chrome.exe' in proc.info['name']:
                return True
        print('Aguardando que o chrome seja aberto pelo usuário')
        return False


    def download_audio(self, driver, element):
        try:
            if element:
                # Create an action chain
                action = ActionChains(driver)
                
                # Scroll to the element to make sure it's in the viewport
                driver.execute_script("arguments[0].scrollIntoView(true);", element)

                hover_script = """
                var event = new MouseEvent('mouseover', {
                    view: window,
                    bubbles: true,
                    cancelable: true
                });
                arguments[0].dispatchEvent(event);
                """
                driver.execute_script(hover_script, element)
                
                addrr_element = "span[data-icon='down-context']"
                element_arrow_down = elements.wait_for_element_to_load(driver, addrr_element, elements.TYPE_FIND_BY_CSS_SELECTOR)
                if element_arrow_down:
                    files = Files()
                    # verificando os arquivos existente
                    files.download_file_prepare()
                    element_arrow_down.click()
                    # verificar o arquivo novo e esperar que ele tenha terminado o download
                    
                    addrr_element = "//div[@aria-label='Baixar' or @aria-label='Download']"

                    element_download = elements.wait_for_element_to_load(driver, addrr_element, elements.TYPE_FIND_BY_XPATH)
                    if element_download:
                        element_download.click()
                        path_file = files.get_downloaded_file()
                        if path_file:
                            return path_file
                
        except Exception as e:
            print(f"An error occurred: {e}")
            return False
        return False
    
