import util.browser_util as browser_util
from selenium.webdriver.common.by import By

articles = []

def get_read_context():
    global articles
    driver = browser_util.capturar_browser()
    try:
        articles_local = driver.find_elements(By.XPATH, "//article[contains(@class, 'w-full') and @class='w-full text-token-text-primary focus-visible:outline-2 focus-visible:outline-offset-[-4px]']")
        if len(articles) == 0:
            articles = articles_local 
            
    except Exception as e:
        print("Erro ao esperar pela resposta:", e)
        
def get_new_item_context():
    global articles
    driver = browser_util.capturar_browser()
    try:
        articles_local = driver.find_elements(By.XPATH, "//article[contains(@class, 'w-full') and @class='w-full text-token-text-primary focus-visible:outline-2 focus-visible:outline-offset-[-4px]']")
        new_articles = [article for article in articles_local if article not in articles]
        return new_articles
    except Exception as e:
        print("Erro ao esperar pela resposta:", e)
        return []
    
    
def get_new_item_context_and_save():
    global articles
    driver = browser_util.capturar_browser()
    try:
        articles_local = driver.find_elements(By.XPATH, "//article[contains(@class, 'w-full') and @class='w-full text-token-text-primary focus-visible:outline-2 focus-visible:outline-offset-[-4px]']")
        new_articles = [article for article in articles_local if article not in articles]
        articles.extend(new_articles)
        return new_articles
    except Exception as e:
        print("Erro ao esperar pela resposta:", e)
        return []