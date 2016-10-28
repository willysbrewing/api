# [START app]
import logging

from flask import Flask


app = Flask(__name__)


@app.route('/mail/send', strict_slashes=False)
def send_mail():
    return 'Send Mail'

@app.route('/mail/check', strict_slashes=False)
def check_mail():
    return 'Check Mail'
