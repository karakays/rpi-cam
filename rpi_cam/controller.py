import time
import io
from io import BufferedReader
from wtforms import BooleanField, validators
from flask_wtf import FlaskForm
from flask import (json,
                   Response,
                   jsonify,
                   redirect,
                   render_template,
                   make_response)

from rpi_cam import app
import capturer
from authenticate import http_auth as auth
from error import BaseError, ValidationError, BaseResponse


class CaptureRequest(FlaskForm):
    stored = BooleanField('store',  validators=[validators.input_required()])


@app.route('/')
def root():
    return redirect("/index.html", code=302)


@app.route('/index.html')
def index():
    return render_template('index.html')


@app.route('/user', methods=['GET'])
@auth
def get_user():
    return json.jsonify(username='selcuk',
                        email='selcuk@eft',
                        id='123123')


@app.route('/capture-disk', methods=['GET'])
def capture_img_disk():
    def image_gen():
        while True:
            delivered = False
            try:
                img = io.open('rpi_cam/static/image.jpeg', 'rb')
                br = BufferedReader(img)
                time.sleep(1)
                yield (
                    b'--frame\r\n' +
                    b'Content-Type: image/jpeg\r\n\r\n' +
                    br.read() +
                    b'\r\n')
                delivered = True
            except IOError as ioe:
                print 'IOError caught: %s' % ioe
            except GeneratorExit as ge:
                print 'GeneratorExit here: %s' % ge
                break
            except Exception as e:
                print 'Exception here: %s' % e
            except:
                print 'Catch all'
            finally:
                if not delivered:
                    print 'delivered failed'
                print 'finally'
        print 'generator stopped'
    return Response(image_gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/capture', methods=['GET'])
def capture():
    response = make_response(capturer.capture_picture())
    response.headers['Content-Type'] = 'image/png'
    response.headers['Content-Disposition'] = 'attachment; filename=image.png'
    return response


@app.route('/capture-cont', methods=['GET'])
def capture_cont():
    img_gen = None  # capturer.capture_picture_cont(0.3)
    return Response(img_gen,
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/live', methods=['GET'])
def stream_live():
    def frame_gen1():
        frame_stream = capturer.stream_live()
        print 'current viewers: %s' % capturer.viewers
        try:
            for frame in frame_stream:
                yield(b'--frame\r\n' +
                      b'Content-Type: image/jpeg\r\n\r\n' +
                      frame +
                      b'\r\n')
        except IOError as ioe:
            print 'IOError caught: %s' % ioe
        except GeneratorExit:
            print 'GeneratorExit caught: handling might come here'
            capturer.disconnect_viewer()
        except Exception as e:
            print 'Exception here: %s' % e
        except:
            print 'Catch all'
        finally:
            print 'finally'
        print 'end of gen: client disconnected handle comes here'

    return Response(frame_gen1(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


def frame_gen():
    frame_stream = capturer.stream_live()
    try:
        yield ''
        for frame in frame_stream:
            yield(b'--frame\r\n' +
                  b'Content-Type: image/jpeg\r\n\r\n' +
                  frame +
                  b'\r\n')
    except GeneratorExit:
        print 'GENERATOR EXIT!!!'


@app.route('/foo', methods=['GET'])
def foo():
    raise BaseError('Critical HW error.')


def read_image(path):
    img = io.open(path, 'rb')
    br = BufferedReader(img)
    return br.read()


@app.errorhandler(RuntimeError)
def handle_exc(error):
    print 'XXXXerror: %s' % error


@app.errorhandler(BaseError)
def handle_base_error(error):
    base_response = BaseResponse(error, 500)
    response = jsonify(base_response.to_dict())
    response.status_code = base_response.status_code
    return response


@app.errorhandler(ValidationError)
def handle_invalid_usage(error):
    base_response = BaseResponse(error, 400)
    response = jsonify(base_response.to_dict())
    response.status_code = base_response.status_code
    return response
