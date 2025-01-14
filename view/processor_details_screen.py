# Class for application Processor Details Screen
# Author: Fernando Abreu e Augusto Rosa
# Date: 01/13/2025
###################################################################################################
# IMPORT
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QApplication, QLabel
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from view.screen import Screen
import datetime
###################################################################################################
# MACROS
## DATA PACKAGE

###################################################################################################
#CLASS

class ProcessorDetailsScreen(Screen):
    def __init__(self, parent: QWidget):
        Screen.__init__(self, parent=parent)
        self.__layout = QVBoxLayout()

        self.graph_cpu_usage = Figure()
        self.axes = self.graph_cpu_usage.add_subplot(111)
        self.canvas_cpu_usage = FigureCanvasQTAgg(self.graph_cpu_usage)

        self.__layout.addWidget(self.canvas_cpu_usage)
        self.setLayout(self.__layout)

        # Criando o Gráfico
    
    def update(self):
        if(self._data is not None):
            dates = [datetime.datetime.fromtimestamp(ts) for ts in self._data[0][0]]

            # Limpa o gráfico antes de adicionar novos dados
            self.axes.cla()

            # Configurações básicas do gráfico
            self.axes.set_title("CPU usage in %")
            self.axes.set_xlabel("time")
            self.axes.set_ylabel("Usage in %")

            # Plotando os novos dados
            self.axes.plot(dates, self._data[0][1], 'r', label="CPU Usage")
            self.axes.legend()  # Adiciona a legenda

            # Ajustar os rótulos do eixo X
            self.axes.set_xticks(dates)  # Define os ticks no eixo X
            self.axes.set_xticklabels([date.strftime('%H:%M:%S') for date in dates], rotation=45)  # Rótulos girados

            # Ajuste dos limites do eixo X para ocupar o gráfico inteiro
            self.axes.set_xlim([dates[0], dates[-1]])

            # Redesenhar o gráfico
            self.canvas_cpu_usage.draw()

            # Resetar os dados
            self._data = None

###################################################################################################

