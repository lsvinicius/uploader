import hashlib
import logging
import os
from collections import namedtuple
from enum import Enum

import magic
from pymongo import MongoClient

import config
from exceptions import FileTooLarge, InvalidType, AlreadyUploaded

if not os.path.exists(config.LOG_FOLDER):
    os.mkdir(config.LOG_FOLDER, mode=0x777)

logging.basicConfig(
    filename=os.path.join(config.LOG_FOLDER, 'log.txt'),
    level=logging.DEBUG
)


class FileValidationCodes(Enum):
    OK = 0,
    TOO_LARGE = 1,
    INVALID_TYPE = 2,
    ALREADY_UPLOADED = 3


UploadedFile = namedtuple('UploadedFile', ['filename', 'sha256'])


class Storage:
    def __init__(self, address: str, port: int, db_name: str):
        self._mongo_conn = MongoClient(address, port)
        self._mongo_db = self._mongo_conn[db_name]

    def add_entry(self, filename: str, content: bytes) -> str:
        sha256 = hashlib.sha256(content).hexdigest()
        self.validate_file(sha256, content)
        self._mongo_db.files.insert_one(
            {'sha256': sha256, 'content': content.decode('UTF-8'), 'filename': filename}
        )
        logging.info('Uploaded file %s correctly', sha256)
        return sha256

    def all_files(self):
        files_col = self._mongo_db['files']
        result = []
        for file in files_col.find({}):
            result.append(UploadedFile(file['filename'], file['sha256']))
        return result

    def validate_file(self, sha256: str, content: bytes):
        validation_code = self._is_valid_file(sha256, content)
        if validation_code == FileValidationCodes.TOO_LARGE:
            logging.debug('File %s too large', sha256)
            raise FileTooLarge()
        if validation_code == FileValidationCodes.INVALID_TYPE:
            logging.debug('File %s should be text', sha256)
            raise InvalidType()
        if validation_code == FileValidationCodes.ALREADY_UPLOADED:
            logging.debug('File %s is already uploaded', sha256)
            raise AlreadyUploaded()

    def _is_valid_file(self, sha256: str, content: bytes) -> FileValidationCodes:
        files_col = self._mongo_db['files']
        if len(content) > config.MAX_FILE_SIZE:
            return FileValidationCodes.TOO_LARGE
        if 'text' not in magic.from_buffer(content):
            return FileValidationCodes.INVALID_TYPE
        if files_col.find_one({'sha256': sha256}):
            return FileValidationCodes.ALREADY_UPLOADED
        return FileValidationCodes.OK
