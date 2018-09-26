try:
	print('Test #1: Try to import library')
	from pyweb import *
except ImportError:
	print('Test #1 failed.')
else:
	print('Test #1 success.')

def test_2():
	print('Test #2: Assert all needed classes are present.')
	try:
		print(BindableFunction)
		print(OLDBindableFunction)
		print(WebServer)
	except:
		print('Test #2 failed.')
	else:
		print('Test #2 success.')
SERVER = None
def test_3():
	print('Test #3: Try to create web server on port 1715.')
	try:
		global SERVER
		SERVER = WebServer(port=1715, debug=True)
	except:
		print('Test #3 failed.')
	else:
		print('Test #3 success.')

def test_4():
	print('Test #4: Try to bind function with URI test_4/')
	try:
		SERVER.bind_old(lambda *x: 'Hello, World!', 'test_4')
	except Exception as e:
		print('Test #4 failed.')
		print(e)
	else:
		print('Test #4 success.')

if __name__ == '__main__':
	test_2()
	test_3()
	test_4()
