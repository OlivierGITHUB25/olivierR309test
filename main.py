import sys
import socket
import time
import threading
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QTextEdit, QPushButton, QMainWindow, QGridLayout, QLineEdit

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        widget = QWidget()
        self.setCentralWidget(widget)
        grid = QGridLayout()
        widget.setLayout(grid)
        self.client_socket = None
        self.compteur = 0
        self.arret_thread = False
        self.good=False

        # Titre fenêtre
        self.setWindowTitle("Chronomètre")

        self.lbl = QLabel(self)
        self.lbl.setText("Compteur:")

        self.champ = QLineEdit(self)
        self.champ.setReadOnly(True)
        self.champ.setText("0")

        self.bouton = QPushButton(self)
        self.bouton.setText("Strart")
        self.bouton.clicked.connect(self.start)

        self.bouton2 = QPushButton(self)
        self.bouton2.setText("Reset")
        self.bouton2.clicked.connect(self.reset)

        self.bouton3 = QPushButton(self)
        self.bouton3.setText("Stop")
        self.bouton3.clicked.connect(self.Stop)

        self.bouton4 = QPushButton(self)
        self.bouton4.setText("Connect")
        self.bouton4.clicked.connect(self.Connect)

        self.bouton5 = QPushButton(self)
        self.bouton5.setText("Quitter")
        self.bouton5.clicked.connect(self.quitter)

        # placement
        grid.addWidget(self.lbl, 1, 1)
        grid.addWidget(self.champ, 2, 1, 1,2)
        grid.addWidget(self.bouton, 3, 1,1,2)
        grid.addWidget(self.bouton2, 4, 1)
        grid.addWidget(self.bouton3, 4, 2)
        grid.addWidget(self.bouton4, 5, 1)
        grid.addWidget(self.bouton5, 5, 2)





    def start(self):
        if self.good == True:
            msg = "start"
            self.client_socket.send(msg.encode())
            self.T1=threading.Thread(target=self.__start)
            self.T1.start()
        else:
            self.T1 = threading.Thread(target=self.__start)
            self.T1.start()

    def __start(self):
        try:
            int(self.compteur)
        except:
            self.champ.setText("pas un int")
            return 0
        while self.arret_thread == False:
            if self.good == True:
                self.compteur = self.compteur + 1
                self.champ.setText(str(self.compteur))
                msg = str(self.compteur)
                self.client_socket.send(msg.encode())
                time.sleep(1)
            else:
                self.compteur = self.compteur + 1
                self.champ.setText(str(self.compteur))
                time.sleep(1)


    def reset(self):
        if self.good == True:
            self.compteur = 0
            self.champ.setText(str(self.compteur))
            msg = "reset"
            self.client_socket.send(msg.encode())
        else:
            self.compteur = 0
            self.champ.setText(str(self.compteur))

    def Stop(self):
        if self.good == True:
            self.arret_thread = True
            self.T1.join()
            msg = "stop"
            self.client_socket.send(msg.encode())
        else:
            self.arret_thread = True
            self.T1.join()



    def quitter(self):
        if self.good == True:
            print ("test")
            msg = "bye"
            self.client_socket.send(msg.encode())
            self.arret_thread = True
            self.T1.join()
            QApplication.exit(0)

        elif self.arret_thread == False:
            self.arret_thread = True
            self.T1.join()
            QApplication.exit(0)
        else:
            QApplication.exit(0)


    def Connect(self):
        host = "localhost"
        port = 10000
        self.client_socket = socket.socket()
        self.client_socket.connect((host, port))
        self.good = True
        print(self.good)

if __name__ == '__main__':

    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()