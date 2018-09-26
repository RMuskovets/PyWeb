import socket

ADDRESS = (HOST, PORT) = ('localhost', 8888)

REQUEST1 = 'GET /test HTTP/1.1'
REQUEST2 = 'HEAD /adasd HTTP/1.1'
REQUEST3 = 'GET /test1 HTTP/1.1'

def test_req_1():
	print('======== TEST 1 ========')
	print('Address: ' + HOST + ':' + str(PORT))
	print('Using request: ' + REQUEST1)
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect(ADDRESS)
	sock.sendall(REQUEST1.encode('utf-8'))
	reply = sock.recv(4096)
	print('== RESPONSE ==')
	print(reply.decode('utf-8'))
	print('======== TEST 1 ========')
	sock.close()

def test_req_2():
	print('======== TEST 2 ========')
	print('Address: ' + HOST + ':' + str(PORT))
	print('Using request: ' + REQUEST2)
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect(ADDRESS)
	sock.sendall(REQUEST2.encode('utf-8'))
	reply = sock.recv(4096)
	print('== RESPONSE ==')
	print(reply.decode('utf-8'))
	print('======== TEST 2 ========')
	sock.close()

def test_req_3():
	print('======== TEST 3 ========')
	print('Address: ' + HOST + ':' + str(PORT))
	print('Using request: ' + REQUEST3)
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect(ADDRESS)
	sock.sendall(REQUEST3.encode('utf-8'))
	reply = sock.recv(4096)
	print('== RESPONSE ==')
	print(reply.decode('utf-8'))
	print('======== TEST 3 ========')
	sock.close()

if __name__ == '__main__':
	print('========= Tests - REQUEST =========')
	test_req_1()
	test_req_2()
	test_req_3()
