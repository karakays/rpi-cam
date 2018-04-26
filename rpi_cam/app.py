import logging
from gevent.wsgi import WSGIServer
from gevent import monkey
from rpi_cam import app

app.secret_key = 'myverylongsecretkey'


def main():
    logging.basicConfig(level=logging.DEBUG)
    app.run('0.0.0.0', 8888, threaded=True)
    # monkey.patch_all()
    # http_server = WSGIServer(('', 8888), app.wsgi_app)
    # http_server.serve_forever()


if __name__ == '__main__':
    main()
