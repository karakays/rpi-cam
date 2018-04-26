import requests
import logging


def get_frame():
    try:
        r = requests.get('http://192.168.1.20:8888/capture', stream=True)
        print r.status_code
        with open('image.jpeg', 'wb') as fd:
            for chunk in r.iter_content(chunk_size=128):
                fd.write(chunk)
    except Exception as e:
        logging.warning('Error received: %s', e)


def init_logger():
    logging.basicConfig(filename='rpi-cam.log',
                        format='%(asctime)s:%(levelname)s:%(message)s',
                        level=logging.WARN)


def main():
    init_logger()
    get_frame()


if __name__ == '__main__':
    main()
