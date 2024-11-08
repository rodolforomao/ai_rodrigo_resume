
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.action_chains import ActionChains

from util.files_util import Files


TYPE_FIND_BY_CLASS = 1
TYPE_FIND_BY_XPATH = 2
TYPE_FIND_BY_CSS_SELECTOR = 3


def wait_for_element_to_load(driver, element_name, type = TYPE_FIND_BY_CLASS, return_element = True, get_list = False, invisible = False, timeout=30, poll_frequency=0.25, error_print = True):
    element = None
    try:
        if type == TYPE_FIND_BY_CLASS:
            typeItem = By.CLASS_NAME
            if invisible:
                element = WebDriverWait(driver, timeout, poll_frequency=poll_frequency).until(
                    EC.invisibility_of_element_located((typeItem, element_name))
                )
            else:
                if get_list:
                        element = WebDriverWait(driver, timeout, poll_frequency=poll_frequency).until(
                        EC.presence_of_all_elements_located((typeItem, element_name))
                    )
                else:
                    element = WebDriverWait(driver, timeout, poll_frequency=poll_frequency).until(
                        EC.presence_of_element_located((typeItem, element_name))
                    )
        elif type == TYPE_FIND_BY_XPATH:
            typeItem = By.XPATH
            if invisible:
                element = WebDriverWait(driver, timeout, poll_frequency=poll_frequency).until(
                    EC.invisibility_of_element_located((typeItem, element_name))
                )
            else:
                if get_list:
                    element = WebDriverWait(driver, timeout, poll_frequency=poll_frequency).until(
                        EC.presence_of_all_elements_located((typeItem, element_name))
                    )
                else:
                    element = WebDriverWait(driver, timeout, poll_frequency=poll_frequency).until(
                        EC.presence_of_element_located((typeItem, element_name))
                    )
        elif type == TYPE_FIND_BY_CSS_SELECTOR:
            typeItem = By.CSS_SELECTOR
            if invisible:
                element = WebDriverWait(driver, timeout, poll_frequency=poll_frequency).until(
                    EC.invisibility_of_element_located((typeItem, element_name))
                )
            else:
                if get_list:
                    element = WebDriverWait(driver, timeout, poll_frequency=poll_frequency).until(
                        EC.presence_of_all_elements_located((typeItem, element_name))
                    )
                else:
                    element = WebDriverWait(driver, timeout, poll_frequency=poll_frequency).until(
                        EC.presence_of_element_located((typeItem, element_name))
                    )
            
        if return_element:
            return element
        
        return True
    except Exception as e:
        if error_print:
            print(f"Erro: O elemento '{element_name}' não foi carregada no tempo especificado.")
            print(e)
    return False


def move_mouse_to_element(driver, element):
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
            element_arrow_down = wait_for_element_to_load(driver, addrr_element, TYPE_FIND_BY_CSS_SELECTOR)
            if element_arrow_down:
                files = Files()
                # verificando os arquivos existente
                files.download_file_prepare()
                element_arrow_down.click()
                # verificar o arquivo novo e esperar que ele tenha terminado o download
                
                addrr_element = "//div[text()='Baixar' or @aria-label='Baixar']"
                element_download = wait_for_element_to_load(driver, addrr_element, TYPE_FIND_BY_XPATH)
                if element_download:
                    element_download.click()
                    path_file = files.get_downloaded_file()
                    if path_file:
                        return True
            
    except Exception as e:
        print(f"An error occurred: {e}")
        return False
    return False