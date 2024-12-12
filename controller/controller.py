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
import view.view
###################################################################################################
# MACROS
###################################################################################################
# GLOBAL VARIABLE
###################################################################################################
buffer_general_screen_data: queue.Queue = queue.Queue()
###################################################################################################
class Controller:

    __view : view.view.View = None

    __model : Model = None

    __lock: threading.Lock = None

    def __init__(self) -> None:
        self.__view: view.view.View = None
        self.__model: Model = None
        self.__lock = threading.Lock()
    
    def connect(self, view: view.view.View, model: Model) -> None:
        self.__view = view
        self.__model = model
    
    def __update(self) -> None:
        s = time.time()
        while(True):
            e = time.time()
            if(e-s > 5.0):
                with self.__lock:
                    thread_update = threading.Thread(target=self.__model.update, name="update data...")
                    thread_update.start()
                    thread_update.join()
                s = time.time()

    def updateDataFromModel(self) -> None:
        thread = threading.Thread(target=self.__update, name='update')
        thread.daemon = True
        thread.start()
    '''
        Métodos de Requisições de dados do view e recebendo a resposta do Model.
    '''

    def dataRequestFromTheGeneralScreen(self):
        request_thread = threading.Thread(target=self.__model.dataRequestFromTheGeneralScreen, name="Data Request Model")
        response_thread = threading.Thread(target=self.__view.update, name="Data Response Model")
        request_thread.start()
        request_thread.join()
        response_thread.start()
        response_thread.join()
    
# end of the Controller class