import os
from app.database import db_session
from flask import render_template, flash, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from mp3concat import concatAudio
from app import app

UPLOAD_FOLDER = 'app/static/audio'
ALLOWED_EXTENSIONS = set(['jpg','mp3'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


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

@app.route('/player',methods=['GET'])
def player():
    books = {}
    booklist = []
    bookDirs = []
    print(UPLOAD_FOLDER)
    dirs = os.listdir(UPLOAD_FOLDER)
    print('dirs = '+str(dirs))
    for dir in dirs:
        if dir[:1] != '.' and dir[-4:] != '.mp3':
            bookDir = UPLOAD_FOLDER+'/'+dir
            print('bookDir = '+str(bookDir))
            p = os.listdir(bookDir)
            #print('p = '+str(p))
            for i in p:
                if i.endswith('.mp3'):
                    booklist.append(i)
            print('booklist = '+str(booklist))

    # for folder in UPLOAD_FOLDER:
    #     print(folder)
    # return render_template('player.html',title='player',thing=a)
    return render_template('player.html',title='player',booklist=booklist,bookDirs=bookDirs)

@app.route('/audio/<path:path>')
def hello(path):
    print('path = '+path)
    return send_from_directory('audio', path)

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
    return render_template('upload.html', filenames=filenames, title='all the new files')
