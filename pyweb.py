from socket import *
from threading import Thread

def get_path_from_http_request(req):
    print (req)
    first_line = req.decode('utf-8').splitlines()[0]
    http_index = first_line.index(' HTTP')
    get_index = first_line.index('GET ') + 4
    return first_line[get_index:http_index]

class BindableFunction:
    def __init__(self, func, uri, mime='text/plain', custom_headers={}):
        self.method = func
        self.type = mime
        self._headers = custom_headers
        self.uri = uri

    def __call__(self, *args, **kwargs):
        return self.method(*args, **kwargs)

    @property
    def headers(self):
        s = b'Content-Type: ' + str.encode(self.type, 'utf-8')
        for key in self._headers:
            s += str.encode(key, 'utf-8') + b': ' + str.encode(self._headers[key], 'utf-8')
        return s

class WebServer:
    def __init__(self, port=8888, threads=5, address='', debug=False):
        self.functions = []
        self.port = port
        self.thread_count = threads
        self.address = address
        self.debug = debug
    def bind(self, func_object):
        assert isinstance(func_object, BindableFunction)
        self.functions.append(func_object)
    def bind_old(self, func, name):
        self.bind(BindableFunction(func, name))

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
            for fn in self.functions:
                path = '/' + fn.uri
                if path == uri:
                    if debug:
                        print('Found function with binded URI: ' + path)
                    headers = fn.headers
                    text = b'HTTP/1.1 200 OK\n' + headers + b'\n\n' + str.encode(fn(), 'utf-8')
                    if debug:
                        print(text)
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
