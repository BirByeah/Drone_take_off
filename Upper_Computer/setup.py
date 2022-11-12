from UI.upper_computer import *
from UI.socket_upper import *



if __name__ == "__main__":
    app = QApplication(sys.argv)
    uci = Upper_Computer_Initialization_UI()
    sys.exit(app.exec())
    ucu = Upper_Computer_UI()
    scu = Socket_Communication_Upper()