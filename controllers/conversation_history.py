# dependencies
from flask import jsonify
from flask import request
from werkzeug.utils import secure_filename
import os

# utils
from utils.constants import ROUTE_SAVE
from utils.utils import allowed_file

def conversation_history():
    try:
        # get files
        all_files = request.files
        # loop all files
        for i in range(0, len(all_files)):
            # get file
            file_save = all_files[f'file{i}']
            # check extensions file is valid
            if allowed_file(file_save.filename):
                file_name = secure_filename(file_save.filename)
                file_save.save(os.path.join(ROUTE_SAVE, file_name))
        return jsonify({'success': True}), 200
    except Exception as e:
        return jsonify({'error': e.args}), 400
