import sys
import time
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QLabel
from PyQt6.QtGui import QColor, QPalette
from PyQt6.QtCore import Qt, pyqtSignal
import threading
import queue
from PyQt6 import QtCore
from PyQt6 import QtGui
from view import Communicate

from view import View
from model import Model
from controller import Controller

click_event = False
cond_variable = False
lock = threading.Lock()
buffer = queue.Queue()

'''
void Controller_Threads()
{
    while(1)
    {
        if(evento)
            lock
            atualiza_buffer
            aciona_variacao_condicao_view
            unlock
    }
}

void Model_thread()
{
    while(1)
    {
        if(time_atual - time_saved > 5 secs)
            lock
            atualiza_buffer
            aciano_variavel_condicao_view
            unlock
    }
}

void view_thread()
{
    while(1)
        if(variavel_condicao)
            lock
            view.consume() __date
            unlock 
            view.update()

      
}
'''

def controller_thread():
    while(True):
        global click_event
        global buffer
        global lock
        if(click_event):
            lock.acquire()
            print("acessando a thread do controller")
            data = model.dataRequestFromTheGeneralScreen2()
            buffer.put(data)
            lock.release()
            view.communicate.update_signal.emit(data)
            click_event = False
            
def model_thread():
    now_time = time.time()
    while(True):
        global buffer
        global lock
        if((time.time())-now_time > 5):
            print("acessando a thread do model")
            lock.acquire()
            data = model.dataRequestFromTheGeneralScreen2()
            buffer.put(data)
            lock.release()
            view.communicate.update_signal.emit(data)
            now_time = time.time()

def view_thread():
    while(True):
        #global cond_variable
            if(not buffer.empty()):
                print("acessando a thread do view")
                lock.acquire()
                data = buffer.get()
                lock.release()
                view.communicate.update_signal.emit(data)




if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Criando as instancias da aplicação do padrão MVC(Model-View-Controller)
    view = View(app)
    model = Model()
    controller = Controller()

    # Fazendo configurações iniciais...
    # P.S.: A ordem importa das conexões.
    controller.connect(model=model)
    view.connect(controller=controller)

    def eventclickGeneralButton():
        view.headerGeneralButtonClickEvent()
        global click_event
        click_event = True
    view.addEventClickGeneralButton(eventclickGeneralButton)

    '''
        Executando a Thread de atualização dos dados do Model em cada 5s
    '''


    #    controller.updateDataFromModel() 

    m_thread = threading.Thread(target=model_thread)
    c_thread = threading.Thread(target=controller_thread)
    v_thread = threading.Thread(target=view_thread)
    m_thread.daemon = True
    c_thread.daemon = True
    v_thread.daemon = True

    m_thread.start()
    c_thread.start()
    v_thread.start()

    '''
        Executando, de forma automatizada pela biblioteca PyQt6, a aplicação.
        P.S.: O loop de execução do programa esta sendo executado nos bastidores pelo encapsulamento e automatização do PyQt6
    '''

    view.run()

    # The End