from socket_communication.upper_computer import *
from socket_communication.socket_upper import *



if __name__ == "__main__":
    app = QApplication(sys.argv)
    uci = Upper_Computer_Initialization_UI()
    sys.exit(app.exec())
    ucu = Upper_Computer_UI()
    scu = Socket_Communication_Upper()