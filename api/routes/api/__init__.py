
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from flask import jsonify

# GENERIC Error

def error(status=400, detail='Bad Request'):
    return jsonify({
        'status': status,
        'detail': detail
    }), status
