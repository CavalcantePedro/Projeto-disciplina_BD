from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget

class MainWindow(QMainWindow):
    
    #Construtor
    def __init__(self, parent:QWidget | None = None, *args, **kwargs) -> None:
        super().__init__(parent, *args, **kwargs)

        #Titulo da janela
        self.setWindowTitle("My App")

        #Layout principal
        self.cw = QWidget()
        self.vLayout = QVBoxLayout()
        self.cw.setLayout (self.v_layout)
        self.setCentralWidget(self.cw)

    #metodo para adicionar um widget no layout principal
    def adicionarWidgetNoVlayout(self, widget: QWidget):
        self.vLayout.addWidget(widget)

    