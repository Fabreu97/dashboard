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

    def __init__(self) -> None:
        self.__model: Model = None
        self.__lock = threading.Lock()
    
    def connect(self, model: Model) -> None:
        self.__model = model
    
    def __update(self) -> None:
        s = time.time()
        while(True):
            e = time.time()
            if(e-s > UPDATE_TIME):
                self.__lock.acquire()
                self.__model.update()
                self.__lock.release()
                s = time.time()
                print("Atualizando os dados do Model")

    def updateDataFromModel(self) -> None:
        thread = threading.Thread(target=self.__update, name='update')
        thread.daemon = True
        thread.start()
    '''
        Métodos de Requisições de dados do view e recebendo a resposta do Model.
    '''

    def dataRequestFromTheGeneralScreen(self):
        request_thread = threading.Thread(target=self.__model.dataRequestFromTheGeneralScreen, name="Data Request Model")
        request_thread.start()
        request_thread.join()
    
# end of the Controller class