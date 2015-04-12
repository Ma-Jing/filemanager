#!/usr/bin/env python
# -*- coding:utf-8 -*-
# all the imports

import os,sys
from flask import Flask, request, session, g, redirect, url_for, \
	abort, render_template, flash

from werkzeug import secure_filename
from contextlib import closing
reload(sys)
sys.setdefaultencoding('utf8')

# configuration
DEBUG = True
SECRET_KEY = 'development key' 
USERNAME = 'admin'
PASSWORD = 'admin'
UPLOAD_FOLDER = '/data/www/files'

# create application
app = Flask(__name__)
app.config.from_object(__name__)
# app.config.from_envvar('FLASKR_SETTINGS', slient=True)

def get_expire_time(file):
    return "OK"

@app.route('/')
def show_entries():
    if not session.get('logged_in'):
        flash('上传文件需先登录')
    entries = {}
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    if files:
        entries = [dict(file=file, time=get_expire_time(file)) for file in files]
    return render_template('show_entries.html', entries=entries)

@app.route('/upload', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('New entry was successfully posted')
        else:
            flash('No file selected')
    return redirect(url_for('show_entries'))

@app.route('/login', methods=['GET','POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            log_user = request.form['username']
            session['logged_in'] = True
            flash('Welcome, %s' % log_user)
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)
    
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('login'))


if __name__  == '__main__':
    app.run(host='0.0.0.0')

