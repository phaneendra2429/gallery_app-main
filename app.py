"""
A sample Hello World server.
"""
import os

from flask import Flask, render_template, request, render_template_string, session, redirect, flash
from PIL import Image
from PIL.ExifTags import TAGS
from google.cloud import storage
from google.cloud import datastore
import datetime
from io import BytesIO
import os
from markupsafe import Markup
import firebase_admin
import pyrebase
from pyrebase import initialize_app
import json
from firebase_admin import credentials, auth





os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "credentials.json"

datastore_client = datastore.Client()
storage_client = storage.Client()
source_bucket_name = 'proj2_phani'     
source_bucket = storage_client.bucket(source_bucket_name)

# Create a client object
#datastore_client = datastore.Client()
# Define the entity kind
#kind = 'image_logs'
# Create a key object for the new entity
#key = datastore_client.key(kind)


# pylint: disable=C0103
app = Flask(__name__)

firebaseConfig = {
    'apiKey': "AIzaSyA4N64aiZN_KZt-8JIppmi9tUw4GevKgQk",
    'authDomain': "mygallery-375619.firebaseapp.com",
    'projectId': "mygallery-375619",
    'storageBucket': "mygallery-375619.appspot.com",
    'messagingSenderId': "26241122008",
    'appId': "1:26241122008:web:a781d63c09bc2c414361ad",
    'measurementId': "G-6VQK3M4495",
    'databaseURL':" "
  }

#Initializing Firebase Authentication
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

app.secret_key = 'Ammu'

@app.route('/')
def login():
    if ('user' in session):
        return redirect('/gallery')    
    return render_template('login.html',code={'name': 0})

@app.route('/', methods=['POST'])
def login_post():
    # if ('user' in session):
    #     return 'Hi you are in the new page'
    if request.method =='POST':
        email = request.form.get('email')
        password = request.form.get('password')
        # print("login",email,password)
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            session['user'] = email
            print('Signedin')
            return redirect('/gallery')
        except:
            print('Unable to signin')
            return render_template('login2.html')
    return render_template('login.html')

@app.route('/google_login')
def google_login():
    # Code to initiate Google login here
    # For example, redirect to a Google login page using the Firebase SDK
    return redirect('/')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def signup_post():
    email = request.form['email']
    password = request.form['password']
    print(email,password)
    try:
        user = auth.create_user_with_email_and_password(email, password)
        session['user'] = email
        # create_folder(email)
        print(create_folder(email))
        return redirect('/gallery')
    except:
        # print('except')
        return render_template('signup2.html')


@app.route('/gallery')
def gallery():
    if 'user' in session:
        user = session['user']
        # fld = user['email']
        print(user)
        bucket = storage_client.bucket('proj2_phani')
        blobs = bucket.list_blobs(prefix=user, delimiter = user+'/') 
        blobs = list(blobs) 
        blobs.pop(0)
        # print(blobs.pop())
        url_lst=[]
        name_lst=[]   
        zp = zip()
        for blb in blobs:
            # blb=next(blobs)
            image_blob = bucket.blob(blb.name)        
            url = image_blob.generate_signed_url(datetime.timedelta(minutes=15))
            url_lst.append(url)
            name_lst.append(blb.name)
            print("this is the name list",name_lst)
            zp = zip(url_lst,name_lst)
        # table_html = create_image_table(url_lst)
    else:
        return render_template('login.html')        
    return render_template('index.html' , image_urls=zp)




@app.route('/gallery', methods=['GET','POST'])
def upload():
    user = session['user']
    if request.method == 'POST':
        
        # Get the file from the request
        file = request.files['image']
        # if file.filename == '':
        #     flash('No image selected!')
        #     return render_template('index.html' , code=1)
        name = file.filename.split('.')[0]

        # Get the source and destination buckets
        blob = source_bucket.blob(user + '/' + name+'.jpeg')     
        blob.upload_from_file(file)

    return redirect('/gallery')


@app.route('/gallery/<path:file_name>')
def get_image_info(file_name):
    file_name = file_name.split('/')[1]
    # print(file_name)    
    if 'user' in session:
        user = session['user']
        blob = source_bucket.blob(user + '/' + file_name)        
        url = blob.generate_signed_url(datetime.timedelta(minutes=15))
        
         exif_dict = {}

        if exifdata:
            for tag_id in exifdata:
                tag = TAGS.get(tag_id, tag_id)
                value = exifdata.get(tag_id)
                if isinstance(value, bytes):
                    try:
                        value = value.decode()
                    except UnicodeDecodeError:
                        pass
                exif_dict[tag] = value

        print('This is a EXIF dictionary',exif_dict)
        
        # exif_dict = json.loads(exif_dict)

        # exif_dict = ndb.model.Expando(**exif_dict).to_dict()
                
        datastore_client = datastore.Client()
        key = datastore_client.key('data', file_name)
        task = datastore.Entity(key)
        task.update({
            'User' : user,
            'Name': file_name,
            'URL' : url,
            'Exif': exif_dict
        })
        # task.update(exif_dict)
        print('This is the task Dictionary',task)
        type(task)
        try: 
            datastore_client.put(task)    
        except:
            exif_dict = str(exif_dict)
            task.update({
            'User' : user,
            'Name': file_name,
            'URL' : url,
            'Exif': exif_dict
            })
            datastore_client.put(task) 

        
        # Download the image from the blob as a byte stream
        image_bytes = BytesIO()
        blob.download_to_file(image_bytes)
        image_bytes.seek(0)

        # Load the image from the byte stream and retrieve the EXIF data
        with Image.open(image_bytes) as img:
            exifdata = img.getexif()
        
       
        # return image_html
        return render_template('view.html', file_name=file_name, url = url, exifdata = exifdata, blob = blob , TAGS=TAGS)
    return render_template('login.html')

@app.route('/delete/<path:file_name>')
def delete(file_name):
    user = session['user']
    blob = source_bucket.blob(user + '/' + file_name)
    blob.delete()
    return redirect('/gallery')

@app.route('/logout')
def logout():
    # Clear the session data
    session.clear()

    # Redirect to the login page
    return render_template('login.html')

def create_folder(folder_name):
    # Get the bucket from Google Cloud Storage
    # bucket = client.bucket(source_bucket_name)
    bucket=source_bucket

    # Check if the folder already exists
    if not bucket.get_blob(folder_name + '/'):
        # Create a new blob with the folder name
        blob = bucket.blob(folder_name + '/')
        blob.upload_from_string('')
        return f'Folder {folder_name} created successfully'
    else:
        return f'Folder {folder_name} already exists'

  

if __name__ == '__main__':
    server_port = int(os.environ.get('PORT', 8080))
    app.run(debug=True, port=server_port, host='0.0.0.0')
