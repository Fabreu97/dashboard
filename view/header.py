# Dashboard Window Header
# Authors: Fernando Abreu e Augusto Rosa
# Date: 12/09/2024
###################################################################################################
# IMPORT
from PyQt6.QtWidgets import QWidget, QPushButton
###################################################################################################
# MACROS
GENERAL_BUTTON_CLICKED = 0
PROCESSOR_BUTTON_CLICKED = 1
MEMORY_BUTTON_CLICKED = 2
PROCESS_BUTTON_CLICKED = 3

GENERAL_BUTTON_NAME: str = "General"
PROCESSOR_BUTTON_NAME: str = "CPU"
MEMORY_BUTTON_NAME: str = "RAM"
PROCESS_BUTTON_NAME: str = "Process"

INITIAL_POSITION_BUTTON_X: int = 10
INITIAL_POSITION_BUTTON_Y: int = 0
BUTTON_SIZE_X: int = 130
BUTTON_SIZE_Y: int = 30

###################################################################################################

class Header:

    __generalButton : QPushButton = None
    
    __processor_details_screen_button : QPushButton = None

    __memory_details_screen_button : QPushButton = None

    __process_details_screen_button : QPushButton = None

    def __init__(self, window: QWidget) -> None:
        self__window = window
        self.__generalButton = QPushButton(GENERAL_BUTTON_NAME, window)
        self.__generalButton.setGeometry(INITIAL_POSITION_BUTTON_X,INITIAL_POSITION_BUTTON_Y, BUTTON_SIZE_X, BUTTON_SIZE_Y) # POS, SIZE
        self.__generalButton.show()

        pos_x = INITIAL_POSITION_BUTTON_X + BUTTON_SIZE_X * 1
        pos_y = INITIAL_POSITION_BUTTON_Y
        self.__processor_details_screen_button = QPushButton(PROCESSOR_BUTTON_NAME, window)
        self.__processor_details_screen_button.setGeometry(pos_x, pos_y, BUTTON_SIZE_X, BUTTON_SIZE_Y) # POS, SIZE
        self.__processor_details_screen_button.show()

        pos_x = INITIAL_POSITION_BUTTON_X + BUTTON_SIZE_X * 2
        pos_y = INITIAL_POSITION_BUTTON_Y
        self.__memory_details_screen_button = QPushButton(MEMORY_BUTTON_NAME, window)
        self.__memory_details_screen_button.setGeometry(pos_x, pos_y, BUTTON_SIZE_X, BUTTON_SIZE_Y) # POS, SIZE
        self.__memory_details_screen_button.show()

        pos_x = INITIAL_POSITION_BUTTON_X + BUTTON_SIZE_X * 3
        pos_y = INITIAL_POSITION_BUTTON_Y
        self.__process_details_screen_button = QPushButton(PROCESS_BUTTON_NAME, window)
        self.__process_details_screen_button.setGeometry(pos_x, pos_y, BUTTON_SIZE_X, BUTTON_SIZE_Y) # POS, SIZE
        self.__process_details_screen_button.show()

    def eventClickGeneralButton(self, func) -> None:
        print("Adicionando a função de eventos do Botão Geral.")
        self.__generalButton.clicked.connect(func)
    def eventClickProcessorButton(self, func) -> None:
        self.__processor_details_screen_button.clicked.connect(func)
    def eventClickMemoryButton(self, func) -> None:
        self.__memory_details_screen_button.clicked.connect(func)
    def eventClickProcessButton(self, func) -> None:
        self.__process_details_screen_button.clicked.connect(func)
    
