# controllers/main_controller.py
import time
import json
import types
from application.model.api_model import APIModel
from application.view.view_view import View

from util.whatsapp_util import WhatsappUtils

class AiagenteController:
    def __init__(self):
        self.api_model = APIModel()
        
        self.view = View()
        self.schedule_sent_status = []

    #def iniciar(self, msg = None, answer_loop = True, assistent_id = None, run_id = None, thread_id = None):
    def iniciar(self, msg = None, answer_loop = True, assistent_id = None):
        resposta = None
        try:
            # if run_id is not None and run_id:
            #     self.api_model.run_id = run_id
            # if thread_id is not None and thread_id:
            #     self.api_model.thread_id = thread_id
            while True:
                output_text = None
                if msg is None:
                    msg = self.view.capturar_resposta()
                elif isinstance(msg, dict):
                    pergunta = msg['message']
                    number = msg['number']
                    if number:
                        whatsapputils = WhatsappUtils()
                        self.api_model.thread_id, self.api_model.run_id  = whatsapputils.get_thread_and_run_ids(number)
                
                if not self.api_model.thread_id and not self.api_model.run_id:
                    request_response = self.api_model.criar_run(pergunta, assistent_id)
                    if number:
                        # Salvar thread e run no arquivo .json
                        whatsapputils = WhatsappUtils()
                        whatsapputils.get_exists_conversation_and_update_thread_run(number, self.api_model.run_id, self.api_model.thread_id)
                else:
                    request_response = self.api_model.criar_mensagem(pergunta)
                    if 'error' in request_response:
                        message = request_response['error'].get('message')
                        if message:
                            print(message)
                    self.api_model.manter_run(assistent_id)
                    if number:
                        # Salvar run no arquivo .json
                        whatsapputils = WhatsappUtils()
                        whatsapputils.get_exists_conversation_and_update_thread_run(number, self.api_model.run_id)

                aguardando_resposta = True
                toggleMsg = True
                
                while aguardando_resposta:
                    time.sleep(0.5)
                    retrive_response = self.api_model.obter_status_run_retrieve()
                    if retrive_response:
                        run_status = retrive_response.get('status')
                        if run_status == "completed":
                            aguardando_recuperacao_mensagem = True
                            while aguardando_recuperacao_mensagem:
                                time.sleep(0.5)
                                resposta = self.api_model.obter_mensagem()
                                if resposta != pergunta:
                                    self.view.exibir_resposta(resposta)
                                    aguardando_recuperacao_mensagem = False
                                    aguardando_resposta = False
                                else:
                                    print('Aguardando resposta')
                        if run_status == "required_action":
                            function_name = self.api_model.get_function_properties(retrive_response)
                            self.view.tratar_status(run_status)
                        if run_status == "requires_action":
                            qnt_requires_actions = self.api_model.get_qnty_actions(retrive_response)
                            calls_ids = []
                            output_responses = []
                            for index in range(qnt_requires_actions):
                                function_name = self.api_model.get_function_properties(retrive_response,'name', index)
                                function_json = self.api_model.get_function_properties(retrive_response,'arguments', index)
                                function_call_id = self.api_model.get_function_properties(retrive_response,'id', index, call_id = True)
                                calls_ids.append(function_call_id)
                                    
                                    
                                self.view.tratar_status(run_status)

                            if calls_ids and output_responses:
                                requests_util = RequestsUtil(self)
                                response_submit_tool_output = requests_util.request_submit_tool(output_responses, calls_ids)
                                
                        if run_status == "in_progress":
                            if toggleMsg:
                                self.view.tratar_status(run_status)
                            toggleMsg = not toggleMsg
                        if run_status == "failed":
                            self.view.tratar_status(run_status)
                            aguardando_recuperacao_mensagem = False
                            aguardando_resposta = False
                            self.view.exibir_resposta(retrive_response.get('error'))
                            resposta = "Status: Falha. OpenAi não disponível no momento."
                            print('Tente novamente mais tarde.')
                        else:
                            self.view.tratar_status(run_status)
                            
                if answer_loop is False:
                    if resposta is None:
                        resposta = output_text
                    if resposta:
                        return resposta,self.api_model.run_id, self.api_model.thread_id
                    return resposta, self.api_model.run_id, self.api_model.thread_id
        except Exception as e:
            print(e)
            
        return resposta, self.api_model.run_id, self.api_model.thread_id
    