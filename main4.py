import sys
import os
import bluetooth
import threading

server_sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
port = 1
server_sock.bind(("",port))
server_sock.listen(1)
connected  = False
DEBUG = True
width = 54
height = 20

STORE_ARR = [["0x00000" for j in range(width)] for i in range(height)]


def render_view():
    for line in STORE_ARR:
        print("%s" %  ";".join(line))

def main():
    while True:
        client_sock, client_info = server_sock.accept()
        if not connected:
            if DEBUG:
                print(client_info, ": connection accepted")
            rt = receiveThread(client_sock, client_info)
            rt.setDaemon(True)
            rt.start()
        else:
           pass
    server_sock.close()
    print("all done")
 
class receiveThread(threading.Thread):

    def __init__ (self,sock,client_info):
        threading.Thread.__init__(self)
        self.sock = sock
        self.client_info = client_info
        connected = True 

    def parse_data(self, s):
        s = s.decode("utf-8")
        arr = s.split("\r\n")
        arr2 = []
        for x in arr:
            x = x.strip()
            if x == '':
               continue
            arr1 = x.split(';')
            for x in arr1:
                if x == '':
                    continue
                arr2.append(x)
        return arr2

    def parse_draw_command(self,s):
        #draw 0xFFFFFF,17:18;
        color = 0
        x = 0
        y = 0
        try:
            arr = s.split(' ')
            (color,location) = arr[1].split(',')
            (y,x) = location.split(':')
            x = int(x)
            y = int(y)
            return (color,x,y)
        except:
            return False

    def run(self):
        try:
            while True:
                data = self.sock.recv(1024)
                if len(data) == 0: break
                if DEBUG:
                    print(self.client_info, ": received [%s]" % data)
                for command in self.parse_data(data):
                    if DEBUG:
                        print(command)
                    if command.startswith('draw '):
                        try:
                            (color,x,y) = self.parse_draw_command(command)
                            STORE_ARR[x][y] = color
                            render_view()
                        except:
                            print(sys.exc_info())
                            print("wrong draw command %s" % command)
                        
        except IOError:
            pass
        self.sock.close()
        if DEBUG:
            print(self.client_info, ": disconnected")
        connected = False

if __name__ == "__main__":
    main()