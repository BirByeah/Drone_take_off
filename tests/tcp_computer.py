import socket
import threading
import sys

class TCP_Computer:
    """
    I suppose that upper is the computer, 
    and it is server.
    """
    def __init__(self, ip, port) -> None:
        self.ip = ip
        self.port = port
        self.integrated_addr = (self.ip, self.port) # Attention! This is for computer itself!
        self.thread_receive = threading.Thread(None, self.receive, "receive")
    
    def connect(self):
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.s.bind(self.integrated_addr)
        self.s.listen(1)
        self.client, self.client_addr = self.s.accept()
        print(f"Connected successfully! The address and ip for the client is {self.client_addr[0]} and {self.client_addr[1]}.")
        self.thread_receive.start()
        
    def receive(self):
        while True:
            recv_data = self.client.recv(1024).decode("utf-8", "ignore")
            if recv_data == "Exit":
               self.deliver("OK, trying to close this connection...")
               self.client.close()
               self.s.close()
               sys.exit(0)
            else:
                print(f"Get:{recv_data}.")
                self.deliver(f"Server Get:{recv_data}.")
               
    def deliver(self,
                context:str):
        try:
            self.client.send(context.encode("utf-8"))
        except UnicodeEncodeError:
            print("Decode error!")
    
if __name__ == "__main__":
    tcp_computer = TCP_Computer("", 5199)
    tcp_computer.connect()