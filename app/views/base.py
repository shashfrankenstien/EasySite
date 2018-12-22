from app import app
from flask import send_file
import os

WEB = app.config['WEB']

MIME_MAP = {
	'js': 'application/javascript',
	'css': 'text/css',
	'html': 'text/html',
	'png':'image/png',
	'jpg': 'image/jpeg',
	'jpeg': 'image/jpeg',
	'svg': 'image/svg+xml',
	'ico': 'image/x-icon',
}

@app.route('/', methods=['GET'])
def home():
	return send_file(os.path.join(WEB, 'index.html'))


@app.route('/static/<string:filename>', methods=['GET'])
def webfiles(filename):
	folder = filename.split('.')[-1].strip()
	return send_file(os.path.join(WEB, folder, filename), mimetype=MIME_MAP[folder])
