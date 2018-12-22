from app import app, db
from flask import request
from datetime import datetime as dt
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-d","--debug", help="Start on port 8080 and debug database", action="store_true")
parser.add_argument("-c","--cherry", help="Start using Cherrypy server", action="store_true")
args = parser.parse_args()


@app.after_request
def teardown(response):
	if app.config['LOG']:
		adr = request.environ.get('REMOTE_ADDR')
		mth = request.environ.get('REQUEST_METHOD')
		pth = request.environ.get('PATH_INFO')
		print(f'''{adr} - [{dt.now().strftime('%d/%b/%Y %H:%M:%S')}] - "{mth} {pth}" - {response.status_code}''')
	return response


def run_cherrypy(app, host='0.0.0.0', port=8080, threads=10, debug=False):
	print('ENGINE Logging = True.')
	app.config['LOG'] = True
	import cherrypy
	if not debug: cherrypy.config.update({'engine.autoreload.on' : False})

	cherrypy.tree.graft(app.wsgi_app, '/')
	cherrypy.server.unsubscribe()
	server = cherrypy._cpserver.Server()

	server.socket_host = host
	server.socket_port = port
	server.thread_pool = threads
	server.subscribe()

	if hasattr(cherrypy.engine, "signal_handler"):
		cherrypy.engine.signal_handler.subscribe()
	if hasattr(cherrypy.engine, "console_control_handler"):
		cherrypy.engine.console_control_handler.subscribe()
	
	try:
		cherrypy.engine.start()
		cherrypy.engine.block()
	except KeyboardInterrupt:
		cherrypy.engine.exit()
		raise KeyboardInterrupt()

def run_development(app, host='0.0.0.0', port=8080, threads=1, debug=True):
	app.config['LOG'] = False
	try:
		app.run(host, port, threaded=(threads>0), debug=debug)
	except KeyboardInterrupt:
		print('Exiting...')


if __name__=='__main__':

	HOST = '0.0.0.0'
	PORT = 8080 if args.debug else 80


	if args.cherry:
		try:
			run_cherrypy(app, host=HOST, port=PORT, threads=5, debug=args.debug)
		except KeyboardInterrupt:
			pass
		except Exception as e:
			print(e)
			print("Falling back to Flask server..")
			run_development(app, host=HOST, port=PORT, threads=1, debug=args.debug)
	else:
		run_development(app, host=HOST, port=PORT, threads=1, debug=args.debug)