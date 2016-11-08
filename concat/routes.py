#!/usr/bin/env python

from flask import Flask, flash, url_for, request, render_template, redirect, send_from_directory

from .forms import LoginForm

app = Flask(__name__)
app.config['WTF_CSRF'] = True
app.config['SECRET_KEY'] = "UrqnGnpztN"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = True

@app.route('/')
def home():
    return 'hey yo'
'''
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] !=app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)
'''
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for ID="%s", member_me=%s' %
            (form.openid.data, str(form.remember_me.data)))
        return redirect('index')
    return render_template('forming.html', title='Shine ON', form=form)

@app.route('/index', methods=['GET', 'POST'])
def index(title='WAHT?!'):
    return render_template('index.html',title=title)













if __name__ == '__main__':
    app.run(port=4444)
