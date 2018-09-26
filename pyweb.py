from socket import *
from threading import Thread

def http_request_data(req):
    first_line = req.decode('utf-8').splitlines()[0]
    http_index = first_line.index(' HTTP')
    method = first_line.split()[0]
    get_index = first_line.index(method + ' ') + 4
    return (first_line.split()[1], method)

class BindableFunction:
    def __init__(self, uri, mime='text/plain', custom_headers={}):
        self.uri = uri;self.mime=mime;self.custom_headers=custom_headers

    def do_get(self, request):
        return ''
    def do_post(self, request):
        return ''

    @property
    def headers(self):
        s = b'Content-Type: ' + str.encode(self.mime, 'utf-8')
        for key in self.custom_headers:
            s += str.encode(key, 'utf-8') + b': ' + str.encode(self.custom_headers[key], 'utf-8')
        return s

class OLDBindableFunction(BindableFunction):
    def __init__(self, func, uri, mime='text/plain', custom_headers={}):
        super(OLDBindableFunction, self).__init__(uri, mime=mime, custom_headers=custom_headers)
        self.method = func

    def do_get(self, request):
        return self(request)
    def do_post(self, request):
        return self(request)

    def __call__(self, *args, **kwargs):
        return self.method(*args, **kwargs)

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
        self.bind(OLDBindableFunction(func, name))

    def run(self):
        listen_socket = socket(AF_INET, SOCK_STREAM)
        listen_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        listen_socket.bind((self.address, self.port))
        listen_socket.listen(self.thread_count)
        debug = self.debug
        if debug:
            print('Socket created.')

        def handle_request(conn):
            ret = 0
            request = conn.recv(1024)
            if debug:
                print('Handling request: ' + request.decode())
            uri, method = http_request_data(request)
            if uri == '/shutdown_server':
                ret = 1
            else:
                text = b'HTTP/1.1 200 OK\n\nNot Found'
                if method not in ['GET', 'POST']:
                    text = b'HTTP/1.1 405 Method Not Supported\nAllow: GET, POST'
                else:
                    for fn in self.functions:
                        path = '/' + fn.uri
                        if path == uri:
                            if debug:
                                print('Found function with binded URI: ' + path)
                            headers = fn.headers
                            text = b'HTTP/1.1 200 OK\n' + headers + b'\n\n'# + str.encode(fn(), 'utf-8')
                            func = (fn.do_post if method == 'POST' else (fn.do_get if method == 'GET' else None))
                            text += str.encode(func(request), 'utf-8')
                            break
                            if debug:
                                print(text)
                conn.sendall(text)
            return ret

        def serve():
            needs_to_stop = 0
            while not needs_to_stop:
                client, _ = listen_socket.accept()
                needs_to_stop = handle_request(client)
                client.close()
        for i in range(self.thread_count):
            Thread(target=serve).start()
            if self.debug:
                print('Server with ID %s created.' % str(i))

if __name__ == '__main__':
    server = WebServer()
    server.bind_old(lambda x: 'Hello!', 'test')
    server.run()
