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
###################################################################################################
# MACROS
HEADER_GENERAL_BUTTON_CLICK_EVENT: int = 1
HEADER_PROCESSOR_BUTTON_CLICK_EVENT: int = 2
HEADER_MEMORY_BUTTON_CLICK_EVENT: int = 3
HEADER_PROCESS_BUTTON_CLICK_EVENT: int = 4
QUEUE_MAX_SIZE: int = 10
UPDATE_TIME: float = 2.0
###################################################################################################
# GLOBAL VARIABLE
###################################################################################################
buffer_general_screen_data: queue.Queue = queue.Queue(QUEUE_MAX_SIZE)
buffer_processor_details_screen_data = queue.Queue(QUEUE_MAX_SIZE)
###################################################################################################
class Controller:

    def __init__(self) -> None:
        self.__model: Model = None
        self.__lock = threading.Lock()
        self.update_thread: threading.Thread = None
        self.request_thread: threading.Thread = None
        self.request_thread_processor_screen: threading.Thread = None

    def connect(self, model: Model) -> None:
        self.__model = model
    
    def __update(self) -> None:
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
<<<<<<< HEAD
        request_thread = threading.Thread(target=self.__model.dataRequestFromTheGeneralScreen, name="Data Request Model")
        request_thread.start()
    
    def dataRequestFromTheGeneralScreen2(self):
        return self.__model.dataRequestFromTheGeneralScreen2()
=======
        if(self.__model is not None):
            self.request_thread = threading.Thread(target=self.__model.dataRequestFromTheGeneralScreen, name="dataRequest", daemon=True)
            self.request_thread.start()
        else:
            print("Erro ao inicializar a thread dataRequest por model não está conectado com Controller.")

    def dataRequestFromTheProcessorDetailsScreen(self) -> None:
        if(self.__model is not None):
            self.request_thread_processor_screen = threading.Thread(target=self.__model.dataRequestFromTheProcessorDetailsScreen, name="dataRequestProcessorScreen", daemon=True)
            self.request_thread_processor_screen.start()
        else:
            print("Erro ao inicializar a thread dataRequest por model não está conectado com Controller.")

>>>>>>> the_last_dance
    
# end of the Controller class