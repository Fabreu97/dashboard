# Class for application General Screen
# Author: Fernando Abreu e Augusto Rosa
# Date: 16/02/2025
###################################################################################################
# IMPORT
import os
import time
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTreeView, QListView
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtCore import QModelIndex, Qt, QAbstractItemModel, QThread, pyqtSignal
from view.screen import Screen
###################################################################################################
# MACROS

PERMISSION_MAPPING = ["---", "--x", "-w-", "-wx", "r--", "r-x", "rw-", "rwx"]

#CLASS

from PyQt6.QtCore import QThread, pyqtSignal

class UpdateThread(QThread):
    update_signal = pyqtSignal()  # Sinal para notificar a UI

    def __init__(self, filesystem):
        super().__init__()
        self.filesystem = filesystem

    def run(self):
        self.filesystem.update()
        self.update_signal.emit()  # Emite o sinal para atualizar a UI

class FileMy:
    permissionError = 0
    fileNotFoundError = 0


    def __init__(self, name: str, path: str, size: int, isDir: bool, permission: str, parent):
        self.name = name
        self.path = path
        self.size = size
        self.isDir = isDir
        self.permission = permission
        self.my_files = []
        self.parent = parent
    
    def update(self):
        try:
            names_files = os.listdir(self.path)
            for name_file in names_files:
                path = str(os.path.join(self.path, name_file))
                if not os.path.islink(path):
                    size = 0
                    isDir = os.path.isdir(path)
                    permission = os.stat(path).st_mode & 0o777
                    owner = PERMISSION_MAPPING[(permission >> 6) & 7]  # Owner bits
                    group = PERMISSION_MAPPING[(permission >> 3) & 7]  # Group bits
                    others = PERMISSION_MAPPING[permission & 7]        # Others bits
                    permission = f"{owner}{group}{others}"
                    current_file = FileMy(name_file, path, size, isDir, permission, self)
                    self.my_files.append(current_file)
                    if isDir:
                        current_file.update()
                    else:
                        size = os.stat(path).st_size
                
        except PermissionError:
            #print(f"Permissão Negada: {self.path}")
            FileMy.permissionError += 1
            return
        except FileNotFoundError:
            #print(f"Arquivo Não Encontrado: {self.path}")
            FileMy.fileNotFoundError += 1
            return

class FileSystemModel(QAbstractItemModel):
    def __init__(self, root: FileMy, parent=None):
        super().__init__(parent)
        self.root = root

    def rowCount(self, parent: QModelIndex):
        if not parent.isValid():
            return len(self.root.my_files)
        parent_node = parent.internalPointer()
        return len(parent_node.my_files)

    def columnCount(self, parent: QModelIndex):
        return 3  # Nome, Tamanho, Permissões

    def data(self, index: QModelIndex, role):
        if not index.isValid():
            return None

        node = index.internalPointer()

        if role == Qt.ItemDataRole.DisplayRole:
            if index.column() == 0:
                return node.name
            elif index.column() == 1:
                return f"{node.size} bytes" if not node.isDir else "Diretório"
            elif index.column() == 2:
                return node.permission

        return None

    def index(self, row, column, parent: QModelIndex):
        if not parent.isValid():
            parent_node = self.root
        else:
            parent_node = parent.internalPointer()

        if row < 0 or row >= len(parent_node.my_files):
            return QModelIndex()

        child_node = parent_node.my_files[row]
        return self.createIndex(row, column, child_node)

    def parent(self, index: QModelIndex):
        if not index.isValid():
            return QModelIndex()

        node = index.internalPointer()
        if node.parent is None or node.parent == self.root:
            return QModelIndex()

        return self.createIndex(node.parent.my_files.index(node), 0, node.parent)

    def headerData(self, section, orientation, role):
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return ["Nome", "Tamanho", "Permissões"][section]
        return None


class Directory(Screen):
    def __init__(self, parent: QWidget, data=None):
        Screen.__init__(self, parent=parent)

        # Criar a raiz do sistema de arquivos
        self.__filesystem = FileMy(name="/home", path="/home", size=0, isDir=True, permission="rwxr-xr-x", parent=None)

        # Criar o modelo de sistema de arquivos personalizado
        self.model = FileSystemModel(self.__filesystem)

        self.isTheDataReady = False

        self.__layout = QVBoxLayout()
        self.setLayout(self.__layout)

        # Criar a TreeView e conectar ao modelo correto
        self.__tree_view = QTreeView(parent=self)
        self.__tree_view.setModel(self.model)
        self.__tree_view.setHeaderHidden(False)  # Mostra os cabeçalhos das colunas

        # Criar a visão de lista para exibir arquivos de um diretório selecionado
        self.__file_model = QStandardItemModel()
        self.__file_model.setHorizontalHeaderLabels(["Arquivos", "Tamanho"])
        
        self.__list_view = QListView(parent=self)
        self.__list_view.setModel(self.__file_model)

        # Adicionar widgets ao layout
        self.__layout.addWidget(self.__tree_view)
        self.__layout.addWidget(self.__list_view)

        # Expande automaticamente a raiz do diretório
        self.__tree_view.expand(self.model.index(0, 0, QModelIndex()))

        # Conectar seleção de diretório à atualização da lista de arquivos
        self.__tree_view.selectionModel().selectionChanged.connect(self.onDirectorySelected)

    def updateInformation(self):
        """Atualiza a estrutura de diretórios e recarrega o modelo."""
        self.__filesystem.update()
        self.model.layoutChanged.emit()
        self.isTheDataReady = True

    def onDirectorySelected(self):
        """Atualiza a lista de arquivos quando um diretório for selecionado na árvore."""
        selected_indexes = self.__tree_view.selectedIndexes()
        if not selected_indexes:
            return

        index = selected_indexes[0]  # Pegamos apenas o primeiro índice selecionado
        node = index.internalPointer()  # Recupera o objeto FileMy correspondente

        if node.isDir:
            self.__file_model.removeRows(0, self.__file_model.rowCount())  # Limpa a lista de arquivos

            for file in node.my_files:
                if not file.isDir:  # Apenas arquivos, não diretórios
                    item_name = QStandardItem(file.name)
                    item_size = QStandardItem(f"{file.size} bytes")
                    self.__file_model.appendRow([item_name, item_size])


    
