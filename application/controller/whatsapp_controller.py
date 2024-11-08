# controllers/whatsapp_controller.py

from model.whatsapp_model import WhatsappModel

class WhatsappController:
    def __init__(self):
        pass

    def iniciar(self):
        whatsappmodel = WhatsAppModel()
        whatsappmodel.iniciar()
    
    