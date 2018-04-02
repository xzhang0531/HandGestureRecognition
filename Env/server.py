#!/usr/bin/env python

import imp

from flask import Flask, request, abort

app = Flask(__name__)

userfunc = None

@app.route('/specialize', methods=['POST'])
def load():
    global userfunc
    # load user function from codepath
    codepath = '/userfunc/user'
    userfunc = (imp.load_source('user', codepath)).main
    return ""

@app.route('/', methods=['GET', 'POST', 'PUT', 'HEAD', 'OPTIONS', 'DELETE'])
def f():
    if userfunc == None:
        abort(500)

    return userfunc()

app.run(host='0.0.0.0', port=8888)
