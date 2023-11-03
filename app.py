#app.py
from flask import Flask, render_template, request, redirect, url_for, Response, jsonify
from werkzeug.utils import secure_filename
from detect_and_track import process_video_frame
from flask_socketio import SocketIO, emit
import shutil
import pathlib
import os
import cv2

app = Flask(__name__)
socketio = SocketIO(app)

UPLOAD_FOLDER = 'static/uploads'
OUTPUT_FOLDER = 'static/outputs'
ALLOWED_EXTENSIONS = {'mp4'}

BASE_DIR = pathlib.Path(__file__).parent.absolute()
app.config['UPLOAD_FOLDER'] = BASE_DIR / 'static/uploads'
app.config['OUTPUT_FOLDER'] = BASE_DIR / 'static/outputs'
 

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        filenames = []
        for i in range(1, 5):
            file_key = f'video{i}'
            if file_key not in request.files:
                return redirect(request.url)
            file = request.files[file_key]
            if file.filename == '':
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                filenames.append(filename)
        return redirect(url_for('video_display', filenames=','.join(filenames)))
    return render_template('index.html')

@app.route('/delete_videos_and_back', methods=['POST'])
def delete_videos_and_back():
    shutil.rmtree(app.config['UPLOAD_FOLDER'])
    os.makedirs(app.config['UPLOAD_FOLDER'])
    shutil.rmtree(app.config['OUTPUT_FOLDER'])
    os.makedirs(app.config['OUTPUT_FOLDER'])
    return redirect(url_for('index'))


@app.route('/video_display/<filenames>')
def video_display(filenames):
    filenames = filenames.split(',')
    return render_template('display.html', filenames=filenames)

@app.route('/video_feed/<filename>')
def video_feed(filename):
    def generate():
        video_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        result_path = os.path.join(app.config['OUTPUT_FOLDER'], filename)
        output_video_path = result_path.rsplit('.', 1)[0] + '_processed.mp4'
        output_txt_file = result_path.rsplit('.', 1)[0] + '_processed.txt'

        for frame in process_video_frame(video_path, output_video_path, output_txt_file):
            success, jpeg = cv2.imencode('.jpg', frame)
            if success:
                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

@socketio.on('request_updates')
def handle_request_updates(json, methods=['GET', 'POST']):
    filename = json['filename']
    txt_file = filename.rsplit('.', 1)[0] + '_processed.txt'
    txt_file_path = os.path.join(app.config['OUTPUT_FOLDER'], txt_file)

    def check_for_updates():
        last_mtime = None
        while True:
            if os.path.exists(txt_file_path):
                mtime = os.path.getmtime(txt_file_path)
                if last_mtime is None or mtime > last_mtime:
                    last_mtime = mtime
                    with open(txt_file_path, 'r') as file:
                        content = file.read()
                        socketio.emit('update_text', {'filename': txt_file, 'data': content}, namespace='/')
            socketio.sleep(1)  # 비동기적으로 sleep, 서버의 블로킹을 방지합니다.

    socketio.start_background_task(check_for_updates)

if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=8080, allow_unsafe_werkzeug=True) 