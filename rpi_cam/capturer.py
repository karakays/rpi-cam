import logging
import time
from io import BufferedReader, BytesIO
from threading import Condition
try:
    import picamera
except ImportError:
    pass


JPEG_FRAME_START = b'\xff\xd8'
viewers = 0
camera = None


class SyncedFrameOutput(object):
    def __init__(self):
        self.frame = None
        self.buffer = BytesIO()
        self.frame_lock = Condition()

    def write(self, cam_out):
        if cam_out.startswith(JPEG_FRAME_START):
            # truncate here to capture a whole frame
            self.buffer.truncate()
            with self.frame_lock:
                self.frame = self.buffer.getvalue()
                self.frame_lock.notify_all()
                logging.debug('Notify other of the frame')
            self.buffer.seek(0)
        # continue writing until new frame arrives
        self.buffer.write(cam_out)


synced_stream = SyncedFrameOutput()


def stream_gen(stream):
    br = BufferedReader(stream)
    yield br.read()


def capture_picture():
    global camera
    if not camera:
        camera = picamera.PiCamera()
    img_stream = BytesIO()
    camera.capture(img_stream, 'png', use_video_port=True)
    img_stream.seek(0)
    return img_stream.read()


def capture_picture_cont(n=1):
    img_stream = BytesIO()
    while True:
        time.sleep(n)
        camera.capture(img_stream, 'jpeg')
        # rewind before reading
        img_stream.seek(0)
        yield (
            b'--frame\r\n' +
            b'Content-Type: image/jpeg\r\n\r\n' +
            img_stream.read() + b'\r\n')
        # rewind before capturing next frame
        img_stream.seek(0)
        img_stream.truncate()


def stream_live():
    global viewers, camera
    if not camera:
        camera = picamera.PiCamera()
    if not camera.recording:
        logging.info('camera starts recording.')
        camera.start_recording(synced_stream, format='mjpeg', quality=23)
    viewers += 1
    while True:
        with synced_stream.frame_lock:
            camera.annotate_text = '%s watching' % viewers
            synced_stream.frame_lock.wait()
            logging.debug('yielding a new frame')
            yield synced_stream.frame
    print 'stream_live about to finish!!!'


def disconnect_viewer():
    global viewers, camera
    viewers -= 1
    if not viewers:
        camera.stop_recording()
        close()


def close():
    global camera
    if camera:
        logging.debug('closing camera')
        camera.close()
        camera = None


def record_video():
    vid_stream = BytesIO()
    camera.start_recording(vid_stream, format='h264')
    camera.wait_recording(5)
    camera.stop_recording()
    vid_stream.seek(0)
    return stream_gen(vid_stream)
