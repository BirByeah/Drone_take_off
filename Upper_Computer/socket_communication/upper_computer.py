import sys
import threading
import time
import socket as soc
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox

from UI.ui_MainWindow_DataDisplay import *
from UI.ui_initialization import *
from utility.log import *

greeting = "Hello, upper!"
serial_conn_ok = "Serial opened!"
serial_comm_ok = "Serial started!"
down_address = "192.168.137.139"
down_port = 49903
up_address = "10.11.193.202"
up_port = 203

UDP_CONNECTION = False
SERIAL_CONNECTION = False
SERIAL_RECV_STARTED = False
check_points = (
    UDP_CONNECTION,
    SERIAL_CONNECTION,
    SERIAL_RECV_STARTED,
)

fatal_error = False
error_content = None

socket_recv_buffer = []

class Upper_Computer_Initialization_UI(Ui_Initialization_MainWindow, QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
        self.adjust_window()
        
        self.show()
        self.thread_check_situation = threading.Thread(None, self.check_the_initialization_situation, "check the initialization situation")
        self.thread_check_situation.start()
        while self.thread_check_situation.is_alive():
            time.sleep(0.02)
        if fatal_error:
            sys.exit(0)
        
    def adjust_window(self):
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Tool)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
    def check_the_initialization_situation(self):
        while True:
            if not fatal_error:
                pass
            else:
                QMessageBox.warning(self, "错误提示", f"{error_content}")
                return

class Upper_Computer_UI:
    def __init__(self) -> None:
        app = QApplication(sys.argv)
        
        self.socket_obj:Socket_Communication_Upper = None
        
        self.logger = Logger("UI")
        
        self.all_data_sheet = []
        self.selected_data = []
        self.socket_parse = threading.Thread(None, self.socket_content_parser, "Socket Parser")
       
    def get_waiting_obj(self, socket_obj):
        self.socket_obj = socket_obj
        
    def socket_content_parser(self):
        pass
        

class Socket_Communication_Upper:
    def __init__(self) -> None:
        self.addr_down = (down_address, down_port)
        self.addr_upper = (up_address, up_port)
        
        self.recv_data:str = None
        
        if not self.start_socket_connection():
            return
        
        self.recv_parse_lock = threading.Lock()
        
        self.recv_thread = threading.Thread(None, self.receive, "recv")
        self.recv_thread.start()
        
        if not self.socket_connection_test():
            return
        
        if not self.serial_connection_test():
            return
        
        if not self.serial_communication_test():
            return

    def start_socket_connection(self):
        try:
            self.socket_connection = soc.socket(soc.AF_INET, soc.SOCK_DGRAM)
        except Exception as e:
            self.socket_connection.close()
            error_content = "无法开启UDP连接，请检查网络情况！"
            fatal_error = True
            return False
        self.socket_connection.bind(self.addr_upper)
        return True
        
    def send(self, data:bytes): # data will be used later.
        while True:
            content = input("Send:")
            if content == "exit":
                sys.exit(0)
            content = content.encode("ASCII")
            self.socket_connection.sendto(content, (self.addr_down))
        
    def receive(self):
        while True:
            self.recv_data = self.socket_connection.recvfrom(1024)[0].decode("utf-8")
            print(f"Get:{self.recv_data}")
            
    def socket_connection_test(self):
        tried_time = 0
        success = False
        while not success:
            if tried_time > 5:
                error_content = "多次重连UDP未果，请检查网络与下位机是否正常！"
                fatal_error = True
                return False
            else:
                self.recv_parse_lock.acquire()
                content = socket_recv_buffer.pop(0)
                self.recv_parse_lock.release()
                if content == greeting:
                    success = True
        return True
    
    def serial_connection_test(self):
        tried_time = 0
        success = False
        while not success:
            if tried_time > 5:
                error_content = "串口始终未打开，请检查串口情况！"
                fatal_error = True
                return False
            else:
                self.recv_parse_lock.acquire()
                content = socket_recv_buffer.pop(0)
                self.recv_parse_lock.release()
                if content == serial_conn_ok:
                    success = True
        return True
    
    def serial_communication_test(self):
        tried_time = 0
        success = False
        while not success:
            if tried_time > 5:
                error_content = "串口无法正常通信，请检查串口通信日志！"
                fatal_error = True
                return False
            else:
                self.recv_parse_lock.acquire()
                content = socket_recv_buffer.pop(0)
                self.recv_parse_lock.release()
                if content == serial_comm_ok:
                    success = True
        return True
                

if __name__ == "__main__":
    pass