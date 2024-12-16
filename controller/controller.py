# Class responsible for managing View requests and forwarding Model responses
# Authors: Fernando Abreu e Augusto Rosa
# Date: 12/11/2024
###################################################################################################
# IMPORT
###################################################################################################
import queue
import threading
import time
from model.model import Model
HEADER_GENERAL_BUTTON_CLICK_EVENT: int = 1
HEADER_PROCESSOR_BUTTON_CLICK_EVENT: int = 2
HEADER_MEMORY_BUTTON_CLICK_EVENT: int = 3
HEADER_PROCESS_BUTTON_CLICK_EVENT: int = 4
###################################################################################################
# MACROS
QUEUE_MAX_SIZE: int = 10
UPDATE_TIME: float = 5.0
###################################################################################################
# GLOBAL VARIABLE
###################################################################################################
buffer_general_screen_data: queue.Queue = queue.Queue(QUEUE_MAX_SIZE)
###################################################################################################
class Controller:

    __model : Model = None

    __lock: threading.Lock = None

    update_thread: threading.Thread = None

    request_thread: threading.Thread = None

    def __init__(self) -> None:
        self.__model: Model = None
        self.__lock = threading.Lock()
        self.update_thread: threading.Thread = None
        self.request_thread: threading.Thread = None

    def connect(self, model: Model) -> None:
        self.__model = model
    
    def __update(self) -> None:
        global dataReadyToSend
        s = 0.0
        e = 10.0
        while(True):
            if( (e - s) > UPDATE_TIME ):   
                self.__lock.acquire()
                self.__model.update()
                self.__lock.release()
                print("Atualizando os dados do Model")
                s = time.time()
            e = time.time()
                
    def updateDataFromModel(self) -> None:
        if(self.__model is not None):
            self.update_thread = threading.Thread(target=self.__update, name="updateData", daemon=True)
            self.update_thread.start()
        else:
            print("Erro ao inicializar a thread updateData por model não está conectado com Controller")

    '''
        Métodos de Requisições de dados do view e recebendo a resposta do Model.
    '''

    def dataRequestFromTheGeneralScreen(self) -> None:
        if(self.__model is not None):
            self.request_thread = threading.Thread(target=self.__model.dataRequestFromTheGeneralScreen, name="dataRequest", daemon=True)
            self.request_thread.start()
        else:
            print("Erro ao incializar a thread dataRequest por model não está conectado com Controller.")
    
# end of the Controller class