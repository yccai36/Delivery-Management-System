import socket
import sys
import time
import pickle
from confirm import Confirm
class TCP:
    def __init__(self):
        # Connect the socket to the port where the server is listening
        self.server_address = ('localhost', 10000)
        print('connecting to {} port {}'.format(*self.server_address))

    def checkServer(self):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(self.server_address)
            data = sock.recv(256)
            data = pickle.loads(data)
            print(data)
            confirm = Confirm(data)
            result = confirm.startListening()
            print(result)
            # if no exception thrown, a new page will be invoked
            # Send data
            # message = b'Client received and confirmed'
            message = result.encode()
            print('sending {!r}'.format(message))
            sock.sendall(message)
            print('closing socket')
            sock.close()
            time.sleep(0.3)
        except socket.error as msg:
            # print("Caught exception socket.error : %s" % msg)
            pass

        
    


