import application.model.core_model as core
import application.model.context_model as context

import util.browser_util as browser_util
import util.elements_util as elements

class AiAgentModel:
    
    def __init__(self):
        print(f'Class: {self.__class__.__name__} - constructor')

    def responder_perguntas(self, perguntas):
        driver = browser_util.capturar_browser()
        element = "//li[contains(@data-testid, 'history-item')]//a//div[normalize-space(text())='Agente Residencial Oliveiras']"
        button = elements.wait_for_element_to_load(driver, element, elements.TYPE_FIND_BY_XPATH, True)
        
        # Caso não seja encontrado o Agente do residencial, cria-lo
        button.click()
        context.get_new_item_context_and_save()
            
        for pergunta in perguntas:
            user_msg = pergunta['message']
            context.get_read_context()
            core.send_text(user_msg)
            if pergunta:
                resposta = core.wait_answer()
                break
        if resposta is not None:
            return resposta
        