#################
#### imports ####
#################

import os, pytz
from datetime import datetime, timedelta
from app import models, db, keygenerator, app
from flask import render_template, flash, request, redirect, url_for, jsonify, send_from_directory, g
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash
from mp3concat import concatAudio
from sparkpost import SparkPost
from flask_login import current_user, login_user, logout_user, login_required


################
#### config ####
################

UPLOAD_FOLDER = 'app/static/audio'
ALLOWED_EXTENSIONS = set(['jpg','mp3'])

##########################
#### helper functions ####
##########################

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

################
#### routes ####
################


@app.route('/')
def home():
    return 'hey yo: Audiobook app'

@app.route('/oy')
@login_required
def oy():
    return 'OY!'

@app.before_request
def before_request():
    g.user = current_user

@app.route('/login', methods=['GET', 'POST'])
def login():
    current_user_id = current_user.get_id()
    print('current_user_id = '+str(current_user_id))
    if current_user_id is not None:
        current_user_id = int(current_user_id)
        user_object = db.session.query(models.User).filter_by(id=current_user_id).one()
        flash(user_object.name + ", you are logged in. If this is not you, please login as yourself", "warning")
    else:
        if request.method == 'POST':
            email =  request.form['email']
            password = request.form['password']
            user = db.session.query(models.User).filter_by(email=email).first()
            if not user or not check_password_hash(user.password, password):
                flash("Incorrect email or password")
                return redirect(url_for('login'))
            login_user(user, remember=True)
            flash("Logged in successfully")
            return redirect('player')
    return render_template('login.html', title='Login')

@app.route('/pwresetrq', methods=['GET','POST'])
def pwresetrq():
    if request.method == 'POST':
        if db.session.query(models.User).filter_by(email=request.form['email']).first():
            user = db.session.query(models.User).filter_by(email=request.form['email']).one()
            print('user_id = '+str(user.id))
            if db.session.query(models.PWReset).filter_by(user_id = user.id).first():
               pwalready = (db.session.query(models.PWReset).filter_by(user_id = user.id).first())
            # if the key hasn't been used yet, just send the same key.
               if pwalready.has_activated == False:
                    print('Password has NOT been activated')
                    pwalready.datetime = datetime.now(pytz.utc)
                    key = pwalready.reset_key
               else:
                    print('Password HAS been activated')
                    key = keygenerator.make_key()
                    pwalready.reset_key = key
                    pwalready.datetime = datetime.now(pytz.utc)
                    pwalready.has_activated = False
            else:
                key = keygenerator.make_key()
                user_reset = models.PWReset(reset_key=key, user_id=user.id)
                db.session.add(user_reset)
            db.session.commit()
            sparky = SparkPost() #uses environment var for API
            from_email = 'aubook-pwReset@'+os.environ['SPARKPOST_DOMAIN']
            response = sparky.transmission.send(
              recipients=[
                {'email':request.form['email']
                },
                {'address':{
                  'email':'aaron.poser@gmail.com',
                  'header_to':request.form['email']
                   }
                }
              ],
              text="I heard you forgot your password. \n\nPlease go to: \n http://localhost:5000"+url_for('pwreset', id=str(key)),
              from_email=from_email,
              subject='Reset your aubook password')
            flash('Please check your email for further intructions.')
        else:
           flash("The email provided was never registered.")
    return render_template('pwresetrq.html',title='Password Reset')

@app.route('/pwreset/<id>', methods=['GET','POST'])
def pwreset(id):
    key=id
    pwresetkey = db.session.query(models.PWReset).filter_by(reset_key=id).one()
    made_by = datetime.utcnow().replace(tzinfo=pytz.utc)-timedelta(hours=24)
    if request.method == 'POST':
      if request.form["password"] != request.form["password2"]:
          flash("Your password and password verification didn't match.")
          return redirect(url_for("pwreset", id = id))
      if len(request.form["password"]) < 8:
          flash("Your password needs to be at least 8 characters")
          return redirect(url_for("pwreset", id = id))
      user_reset = db.session.query(models.PWReset).filter_by(reset_key=id).one()
      db.session.query(models.User).filter_by(id = user_reset.user_id).update({'password': generate_password_hash(request.form["password"])})
      user_reset.has_activated = True
      db.session.commit()
      flash("Your new password has been updated saved.")

    if pwresetkey.has_activated is True:
        flash("Your password was already reset with this link.\n\n If you need to set it again, please make a new request below.")
        return redirect(url_for('pwresetrq'))

    if pwresetkey.datetime.replace(tzinfo=pytz.utc) < made_by:
        flash("Your password reset link expired. Please generate a new one below.")
        return redirect(url_for("pwresetrq"))
    return render_template('pwreset.html', id=key,title='Password Reset')


@app.route('/logout')
@login_required
def logout():
    """Logout the current user."""
    logout_user()
    flash('You were logged out.')
    return redirect (url_for('login'))


@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        if not request.form['password'] or not request.form['password2']:
            flash('Please enter and confirm a password')
            return redirect(request.url)
        if request.form['password'] != request.form['password2']:
            flash('Passwords must match')
            return redirect(request.url)
        if len(request.form['password']) < 8:
            flash('The password you provided must have at minimum eight characters')
            return redirect(request.url)
        print('checking to see if user exists')
        user_check = models.User.query.filter_by(email=request.form['email']).first()
        # print('user_check = '+str(user_check))
        if user_check is not None:
            flash('That email is already in use. Either chose a new one or try to reset your password')
            return redirect(request.url)
        user = models.User(name=request.form['name'],
                           password=generate_password_hash(request.form['password']),
                           email=request.form['email'])
        db.session.add(user)
        db.session.commit()
        flash('User successfully registered')
        return redirect(url_for('player'))
    return render_template('register.html',title='Register')


@app.route('/library', methods=['GET','POST'])
@login_required
def library():
    g.user=current_user
    # print('current user id: '+str(current_user.id))
    all_books = db.session.query(models.Book).all()
    currently_checkedout_books = db.session.query(models.BookUser).filter_by(user_id = current_user.id).all()
    print('all books before evaluation:')
    for book in all_books:
        print(book.title,' '+str(book.id))
    print('\n')

    for already_checkedout in currently_checkedout_books:
      for book in all_books:
        if book.id == already_checkedout.book_id:
            all_books.remove(book)
            for book in all_books:
                print(book.title,' '+str(book.id))

    if request.method == 'POST':
           selected_books = request.form.getlist('book')
           if not selected_books:
               flash('You have not selected any books for checkout.')
               return redirect(request.url)
           #print(selected_books)
           for i in selected_books:
            #    print(i)
               book = db.session.query(models.Book).filter_by(id=int(i)).one()
               current_user.books.append(book)
           db.session.commit()
           return redirect(url_for('player'))
               #print(a.title)
           any_selected = bool(selected)
    return render_template('library.html',title='Library',booklist=all_books)


@app.route('/player')
@login_required
def newplayer():
    currently_checkedout_books = []
    g.user=current_user
    checkedout_books_by_user = db.session.query(models.BookUser).filter_by(user_id = current_user.id).all()
    # for e in checkedout_books_by_user:
    #     print('e.book_id = '+str(e.book_id))
    print('\n')
    for entry in checkedout_books_by_user:
        book = db.session.query(models.Book).filter_by(id = entry.book_id).one()
        # print('book type = '+str(type(book)))
        # print('book object = '+str(book))
        # print(book.id)
        # print(book.title)
        currently_checkedout_books.append(book)
    return render_template('player.html',title='player NEW',booklist=currently_checkedout_books,bookInfo=checkedout_books_by_user)




@app.route('/audio/<path:path>')
@login_required
def serve_audio(path):
    # print('path = '+path)
    dir = 'static/audio'
    return send_from_directory(dir, path)


@app.route('/retrieveTime', methods=['POST'])
@login_required
def retrieveTime():
    g.user = current_user
    print('before request')
    print(request.json['book_id'])
    currentBook = db.session.query(models.BookUser).filter_by(user_id = current_user.id, book_id = request.json['book_id']).one()
    print('currentBook.currentTime = '+str(currentBook.currentTime))
    currentBookTime = currentBook.currentTime
    print(type(currentBookTime))
    return jsonify(currentBookTime=currentBookTime)

@app.route('/saveTime', methods=['POST'])
@login_required
def saveTime():
    g.user = current_user
    currentBook = db.session.query(models.BookUser).filter_by(user_id = current_user.id, book_id = request.json['book_id']).one()
    currentBook.currentTime = request.json['currentTime']
    db.session.add(currentBook)
    db.session.commit()
    return ('')

@app.route('/saveBookmark', methods=['POST'])
@login_required
def saveBookmark():
    g.user = current_user
    print(type(request.json['desc']))
    print('desc = '+str(request.json['desc']))
    print('time = '+str(request.json['time']))
    print('book_id = '+str(request.json['book_id']))
    newBookmark = models.Bookmark(desc=request.json['desc'],time=request.json['time'],book_id=request.json['book_id'],user_id=current_user.id)
    db.session.add(newBookmark)
    db.session.commit()
    return ('')


@app.route('/time', methods=['GET','POST'])
@login_required
def posttime():
    g.user = current_user
    print('before request')
    print(request.json['book_id'])
    currentBook = db.session.query(models.BookUser).filter_by(user_id = current_user.id, book_id = request.json['book_id']).one()
    print('currentBook.currentTime = '+str(currentBook.currentTime))
    currentBookTime = currentBook.currentTime
    print(type(currentBookTime))
    return jsonify(currentBookTime=currentBookTime)
    # if request.method == 'GET':
    #     print('book_id = '+str(request.form['book_id']))
    #     # return Response(
    #     #    r.text
    #     #    status=r.status.code,
    #     # )
    #     currentBook = db.session.query(models.BookUser).filter_by(user_id = current_user.id, book_id = request.form['book_id']).one()
    #     currentTime = currentBook.currentTime
    #     return(resp.text, resp.status_code, resp.headers.items(), currentTime)
    # # return ('')
    #
    # if request.method == 'POST':
    #     print('book_id = '+str(request.form['book_id']))
    #     print('currentTime = '+str(request.form['currentTime']))
    #     print('request.data = '+request.data) # returns no data
    #     if request.form['currentTime'] == 'none':
    #         print('no currentTime value provided')
    #         currentBook = db.session.query(models.BookUser).filter_by(user_id = current_user.id, book_id = request.form['book_id']).one()
    #         # c = currentBook.currentTime
    #         # print(c)
    #         return str(currentBook.currentTime)
    #     else:
    #         # print('request.url = '+request.url) # returns no data
    #         # print('request.query_string = '+request.query_string) # returns no data
    #         # print('request.data = '+request.data) # returns no data
    #         print('book_id = '+str(request.form['book_id']))
    #         print('currentTime = '+str(request.form['currentTime']))
    #         # print('request.values[\'id\'] = '+str(request.values['id'])) # returns data when charset = application/json;charset=UTF-8
    #         # print('request.values[\'currentTime\'] = '+str(request.values['currentTime'])) # returns data when charset = application/json;charset=UTF-8
    #         # print('id = '+str(request.args.get('id'))) # returns data when charset = application/json;charset=UTF-8
    #         # print('request.json[\'id\'] = '+request.json['id'])
    #         # print('request.json[\'currentTime\'] = '+str(request.json['currentTime']))
    #         # print('currentTime = '+str(request.args.get('time'))) # returns no data
    #         # print('request.view_args = '+str(request.view_args))  # returns no data
    #         # print('request.get_json = '+str(request.get_json))
    #         # print('request.is_json = '+str(request.is_json))
    #         # print('request.json = '+str(request.json))
    #         # print('request.is_xhr = '+str(request.is_xhr))
    #         # goal is to update BookUser table with new time entry for current_user and book_id
    #         currentBook = db.session.query(models.BookUser).filter_by(user_id = current_user.id, book_id = request.form['book_id']).one()
    #         currentBook.currentTime = request.form['currentTime']
    #         db.session.commit()
        # return ('')
    # return render_template('placeholder.html')


@app.route("/upload", methods=['GET','POST'])
@login_required
def upload():
    g.user = current_user
    filenames = []
    if request.method == 'POST':
        if request.form['title'] == '':
            flash('Please enter a title of the book that is to be uploaded')
            return redirect(request.url)
        newfolder_id = db.session.query(db.func.max(models.Book.id)).scalar() # latest id

        # print('newfolder_id = '+str(newfolder_id))
        newfolder_id = int(newfolder_id or 0 ) + 1
        dir = UPLOAD_FOLDER+'/'+str(newfolder_id)
        # print('dir = '+str(dir))
        uploaded_files = request.files.getlist("file")
        #print('\n')
        shareable = 'shareable' in request.form
        # print('shareable = '+str(shareable))
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
        a = concatAudio(dir,request.form['title'])
        a.concat()
        newBook = models.Book(title=request.form['title'],author=request.form['author'],shareable=shareable)
        current_user.books.append(newBook)
        db.session.add(newBook)
        db.session.commit()
    return render_template('upload.html', filenames=filenames, title='all the new files')
