import socket
import threading
import sys

class TCP_Drone:
    """
    I suppose that down is the drone, 
    and it is client.
    """
    def __init__(self, ip, port) -> None:
        self.ip = ip
        self.port = port
        self.integrated_addr = (self.ip, self.port) # Attention! This is for computer itself!
        self.thread_receive = threading.Thread(None, self.receive, "receive")
        self.thread_deliver = threading.Thread(None, self.deliver, "deliver", "a")
    
    def connect(self):
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.s.connect(self.integrated_addr)
        print(f"Connected successfully!")
        self.thread_receive.start()
        self.thread_deliver.start()
        
    def receive(self):
        while True:
            recv_data = self.s.recv(1024).decode("utf-8", "ignore")
            print(recv_data)
               
    def deliver(self,
                context:str):
        while True:
            context = input("Send:")
            try:
                self.s.send(context.encode("utf-8"))
            except UnicodeEncodeError:
                print("Encode error!")
    
if __name__ == "__main__":
    tcp_drone = TCP_Drone("10.11.195.104", 5199)
    tcp_drone.connect()