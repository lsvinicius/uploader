import os

PORT = 8000
DB_NAME = 'upload_db_stg'
DB_ADDRESS = 'storage'
DB_PORT = 27017
MAX_FILE_SIZE = 15*1024*1024  # Uploaded file size limit 15MB
LOG_FOLDER = os.path.expanduser(os.path.join('~', '.uploader'))
