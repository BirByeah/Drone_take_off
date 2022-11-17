import socket as soc
import threading
import sys

drone_address = "192.168.137.139"
drone_port = 49903
computer_address = "10.11.195.104"
computer = 5199

socket_recv_buffer = None

class UDP_Drone:
    def __init__(self) -> None:
        self.addr_drone = (drone_address, drone_port)
        self.addr_computer = (computer_address, computer)
        
        self.recv_data:str = None
        
        self.start_socket_connection()
        
        self.recv_thread = threading.Thread(None, self.receive, "recv")
        self.recv_thread.start()
        
        self.send_thread = threading.Thread(None, self.send, "send", [None])
        self.send_thread.start()

    def start_socket_connection(self):
        try:
            self.udp = soc.socket(soc.AF_INET, soc.SOCK_DGRAM)
        except Exception as e:
            self.udp.close()
            raise e
        self.udp.bind(self.addr_drone)
        
        
    def send(self, data:bytes): # data will be used later.
        while True:
            content = input("Send:")
            if content == "exit":
                self.udp.close()
                sys.exit(0)
            try:
                content = content.encode("utf-8")
            except UnicodeEncodeError:
                print("Encode error!")
            self.udp.sendto(content, (self.addr_computer))
        
    def receive(self):
        while True:
            self.recv_data = self.udp.recvfrom(1024)[0].decode("utf-8", "ignore")
            print(f"Get:{self.recv_data}")
            

if __name__ == "__main__":
    uc = UDP_Drone()