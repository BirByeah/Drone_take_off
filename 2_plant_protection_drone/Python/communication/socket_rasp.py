import socket as soc
import threading
import sys

down_address = "192.168.137.139"
down_port = 49903
up_address = "10.11.193.202"
up_port = 203

class Socket_Communication_Down:
    def __init__(self) -> None:
        self.addr_upper = (up_address, up_port)
        self.addr_down = (down_address, down_port)
        
        self.recv_data:str = None
        
        self.start_socket_connection()
        
        self.recv_thread = threading.Thread(None, self.receive, "recv")
        self.recv_thread.start()
        
        self.send(None)

    def start_socket_connection(self):
        try:
            self.socket_connection = soc.socket(soc.AF_INET, soc.SOCK_DGRAM)
        except Exception as e:
            self.socket_connection.close()
            raise e
        self.socket_connection.bind(self.addr_down)
        
        
    def send(self, data:bytes): # data will be used later.
        while True:
            content = input("Send:")
            if content == "exit":
                sys.exit(0)
            self.socket_connection.sendto(content.encode("utf-8"), (self.addr_upper))
        
    def receive(self):
        while True:
            self.recv_data = self.socket_connection.recvfrom(1024)[0].decode("ASCII")
            print(f"Get:{self.recv_data}")
            
scd = Socket_Communication_Down()
