import os
from flask import render_template, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from mp3concat import concatAudio
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

        dir = UPLOAD_FOLDER+'/'+request.form['name']

        uploaded_files = request.files.getlist("file")
        print('\n')
        for file in uploaded_files:
            print('file name:')
            print(file.filename)
            if file.filename == '':
              flash('No files selected')
              return redirect(request.url)
            # Check if the file is one of the allowed types/extensions
            if file and allowed_file(file.filename):
                # Make the filename safe, remove unsupported chars
                filename = secure_filename(file.filename)
                # Move the file from the temp folder ot the upload folder
                if not os.path.exists(dir):
                    print('folder does not exist. Creating folder...')
                    os.makedirs(dir)
                print('uploading '+file.filename)
                file.save(os.path.join(dir, filename))
                print('upload of '+filename+' complete')
                # save the filename into a list, we'll use it later
                filenames.append(filename)
            else:
                flash('Only files of type mp3 and jpg will be uploaded.')
                #return redirect(request.url)
        print('\n')
        a = concatAudio(dir,request.form['name'])
        a.concat()
        #cwd = print('cwd = '+os.getcwd())
        #filenames = []
    return render_template('upload.html', filenames=filenames, title='all the new files')
