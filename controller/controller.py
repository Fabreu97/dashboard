# Class responsible for managing View requests and forwarding Model responses
# Authors: Fernando Abreu e Augusto Rosa
# Date: 12/11/2024
###################################################################################################
# IMPORT
import queue
import threading
from ..model.model import Model
from ..view.view import View
###################################################################################################
# MACROS
    
###################################################################################################
# GLOBAL VARIABLE
buffer_general_screen_data: queue.Queue = queue.Queue()

class Controller:

    __view : View = None

    __model : Model = None

    def __init__(self) -> None:
        self.__view: View = None
        self.__model: Model = None
    
    def connect(self, view: View, model: Model) -> None:
        self.__view = view
        self.__model = model

    def dataRequestFromTheGeneralScreen(self):
        

    
# end of the Controller class