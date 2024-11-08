import time
import util.browser_util as browser_util

import application.model.context_model as context

import util.elements_util as elements

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

def send_text(text):
    driver = browser_util.capturar_browser()
    element = "//div[@contenteditable='true' and @id='prompt-textarea']"
    textarea = elements.wait_for_element_to_load(driver,element, elements.TYPE_FIND_BY_XPATH, True)
    if textarea:
        driver.execute_script("arguments[0].style.display = 'block';", textarea)
        
        textarea.send_keys(text)
    
        try:
            send_button = driver.find_element(By.XPATH, "//button[@aria-label='Enviar prompt']")
            if not send_button.is_enabled():
                print("Send button is disabled.")
            else:
                send_button.click()
        except Exception as e:
            print(e)
            
def wait_answer():
    last_article_text = None
    last_article_html = None
    
    driver = browser_util.capturar_browser()
    try:
        watchdog = 0
        watchdog_timeout = 20
        encontrado = False
        iniciourecepcao = False
        while True:
            articles = context.get_new_item_context()
            if len(articles) >= 2 or watchdog > watchdog_timeout:
                for index, article in enumerate(articles):
                    if index == len(articles) - 1:
                        last_article_text = article.text
                        if last_article_text != '' and len(last_article_text) >= 3 and last_article_text != '4o mini':
                            encontrado = True
                            iniciourecepcao = True
                            break
            if encontrado:
                print('Encontrado')
                break
            print('Aguardando resposta')
            time.sleep(1)
            watchdog += 1
        
        tamanho_texto = 0 
        tamanho_texto_anterior = 0 
        watchdog = 0
        watchdog_timeout = 5
        contador = 0
        finalizou = False
        while iniciourecepcao:
            articles = context.get_new_item_context()
            if len(articles) >= 2:
                for index, article in enumerate(articles):
                    if index == len(articles) - 1:
                        #tamanho_texto = len(article.text)
                        tamanho_texto = len(article.get_attribute('innerHTML'))
                            
                        if tamanho_texto_anterior == tamanho_texto:
                            watchdog += 1
                        else:
                            watchdog = 0
                            print('zerando watchdog')
                            
                        if watchdog >= watchdog_timeout:
                            finalizou = True
                            break
                            
                        if tamanho_texto_anterior != tamanho_texto:
                            tamanho_texto_anterior = tamanho_texto
                            
            time.sleep(0.25)            
            if finalizou:
                break
        
        for index, article in enumerate(articles):
            if index == len(articles) - 1:
                last_article_text = article.text
                last_article_html = article.get_attribute('innerHTML')
        # somente sava os novos itens após confirmar o recebimento
        context.get_new_item_context_and_save()
    except Exception as e:
        print("Erro ao esperar pela resposta:", e)
    
    if last_article_html:
        soup = BeautifulSoup(last_article_html, 'html.parser')
        hyperlinks = soup.find_all('a')
        links_texts = []
        for link in hyperlinks:
            href = link.get('href')  # Obtém o link
            text = link.text.strip()  # Obtém o texto associado ao link
            
            if href and text:
                links_texts.append((text, text + "(" + href+ ")"))  # Armazena como tupla (texto, link)

        for text, href in links_texts:
            last_article_text = last_article_text.replace(text, href)
    
    return last_article_text
        

