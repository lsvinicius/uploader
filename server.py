from flask import Flask, request, Response, render_template
import config
from exceptions import AlreadyUploaded, InvalidType, FileTooLarge
from storage_api import Storage

app = Flask(__name__)
storage = Storage(address=config.DB_ADDRESS, port=config.DB_PORT, db_name=config.DB_NAME)


def handle_response(func):
    def run_func():
        try:
            code, msg = func()
        except FileTooLarge as e:
            code, msg = 400, f"Max file size {config.MAX_FILE_SIZE} bytes"
        except InvalidType as e:
            code, msg = 400, "File must have text only"
        except AlreadyUploaded as e:
            code, msg = 400, "File already uploaded"
        return Response(status=code, response=msg)
    return run_func


@app.route("/")
def index():
    return render_template('index.jinja', all_uploaded_files=storage.all_files())


@app.route("/upload", methods=["POST"])
@handle_response
def upload():
    file = request.files['file']
    filename = file.filename
    content = file.read()
    sha256 = storage.add_entry(filename, content)
    return 200, f"Uploaded {sha256} successfully"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=config.PORT)
