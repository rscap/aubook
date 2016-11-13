import os
from flask import render_template, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from app import app

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['jpg','mp3'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return 'hey yo: Audiobook app'

@app.route('/oy')
def oy():
    return 'OY!'

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for ID="%s", member_me=%s' %
            (form.openid.data, str(form.remember_me.data)))
        return redirect('index')
    return render_template('login.html', title='Login', form=form)

@app.route("/upload", methods=['GET','POST'])
def upload():
    filenames = []
    if request.method == 'POST':

        if request.form['name'] == '':
            flash('Please enter file name')
            return redirect(request.url)

        uploaded_files = request.files.getlist("file")
        for file in uploaded_files:
            #print(file.filename)
            if file.filename == '':
              flash('No files selected')
              return redirect(request.url)
            # Check if the file is one of the allowed types/extensions
            if file and allowed_file(file.filename):
                # Make the filename safe, remove unsupported chars
                filename = secure_filename(file.filename)
                # Move the file from the temp folder ot the upload folder
                #file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                file.save(os.path.join(dir, filename))
                # save the filename into a list, we'll use it later
                filenames.append(filename)
            else:
                flash('That file type is not allowed.')
                return redirect(request.url)
            #return redirect(url_for('uploaded_file', filenames=filenames))

        #uploaded_files = request.files.getlist("file")
        name = request.form['name']
        # print('name = '+name)
        # print(UPLOAD_FOLDER)
        dir = UPLOAD_FOLDER+'/'+name
        # print(dir)
        if not os.path.exists(dir):
            print('folder does not exist. Creating folder...')
            os.makedirs(dir)

        filenames = []
        count = 0

    return render_template('upload.html', filenames=filenames, title='all the new files')
