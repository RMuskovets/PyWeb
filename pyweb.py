from socket import *
from threading import Thread

def get_path_from_http_request(req):
    print (req)
    first_line = req.decode('utf-8').splitlines()[0]
    http_index = first_line.index(' HTTP')
    get_index = first_line.index('GET ') + 4
    return first_line[get_index:http_index]

class WebServer:
    def __init__(self, port=8888, threads=5, address='', debug=False):
        self.functions = {}
        self.port = port
        self.thread_count = threads
        self.address = address
        self.debug = debug
    def bind(self, func, name):
        self.functions['/' + name] = func

    def run(self):
        listen_socket = socket(AF_INET, SOCK_STREAM)
        listen_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        listen_socket.bind((self.address, self.port))
        listen_socket.listen(self.thread_count)
        debug = self.debug
        if debug:
            print('Socket created.')

        def handle_request(conn):
            request = conn.recv(1024)
            if debug:
                print('Handling request: ' + request.decode())
            uri = get_path_from_http_request(request)
            text = b'HTTP/1.1 200 OK\n\nNot Found'
            for path in self.functions:
                if path == uri:
                    if debug:
                        print('Found function with binded URI: ' + path)
                    func = self.functions[path]
                    text = b'HTTP/1.1 200 OK\n\n' + eval('b"%s"' % func())
            conn.sendall(text)

        def serve():
            needs_to_stop = 0
            while not needs_to_stop:
                client, _ = listen_socket.accept()
                handle_request(client)
                client.close()
        for i in range(self.thread_count):
            Thread(target=serve).start()
            if self.debug:
                print('Server with ID %s created.' % str(i))

if __name__ == '__main__':
    server = WebServer()
    server.connect(lambda: 'Hello!', 'test')
    server.run()
