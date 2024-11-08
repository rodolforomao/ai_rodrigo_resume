# model/queue_manager.py
        
class QueueController:
    
    def __init__(self):
        print(f'Class: {self.__class__.__name__} - constructor')
        self.perguntas = []  # Lista para armazenar perguntas
        self.perguntas_respondidas = []  # Lista para armazenar perguntas
        self.respostas = []   # Lista para armazenar respostas

    def adicionar_pergunta(self, pergunta):
        self.perguntas.append(pergunta)
        
    def adicionar_pergunta_respondida(self, pergunta):
        self.perguntas_respondidas.append(pergunta)

    def adicionar_resposta(self, resposta):
        self.respostas.append(resposta)

    def processar_perguntas(self):
        while self.perguntas:
            pergunta = self.perguntas.pop(0)
            # Aqui, você pode chamar a função para responder a pergunta
            yield pergunta  # Isso pode ser substituído pela chamada de resposta se necessário
