from flask import Flask, render_template, request, redirect, jsonify, make_response, url_for, flash, session, send_file
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity, unset_jwt_cookies
import hashlib
from werkzeug.security import check_password_hash
from flask_wtf.csrf import CSRFProtect
from datetime import timedelta, datetime
from image_to_vid import *
from backend import *
from PIL import Image
import numpy as np
import base64
import io


def image_to_base64(image):
    # Convert the pixel values to a NumPy array
    np_image = np.array(image, dtype=np.uint8)

    # Convert the NumPy array to a PIL Image
    pil_image = Image.fromarray(np_image)

    # Create a BytesIO object to hold the image data
    image_bytes = io.BytesIO()

    # Save the PIL Image to the BytesIO object as PNG format
    pil_image.save(image_bytes, format='PNG')

    # Encode the image data as base64
    base64_image = base64.b64encode(image_bytes.getvalue()).decode('utf-8')

    return base64_image
# app = Flask(__name__)
# app.config['JWT_SECRET_KEY'] = 'alDkhodRflAkyKhgEaluSioiqa3Cws4OrftgyCujiOk78K452/;[]'
# jwt = JWTManager(app)
# if (db.is_connected):
#     print('lesgo')

app = Flask(__name__)
app.config["JWT_TOKEN_LOCATION"] = ["headers", "cookies", "json", "query_string"]
app.config['JWT_SECRET_KEY'] = 'super-secret'
app.config['JWT_COOKIE_SECURE'] = False
app.secret_key = 'alDkhodRflAkyKhgEaluSioiqa3Cws4OrftgyCujiOk78K452/;[]'
app.config['JWT_ACCESS_COOKIE_PATH'] = '/user'
app.config['JWT_COOKIE_CSRF_PROTECT'] = False
# app.config['JWT_REFRESH_COOKIE_PATH'] = '/login'
# csrf = CSRFProtect(app)

jwt = JWTManager(app)

users = fetch_users()

def get_user_data(username):
    users=fetch_users()
    return users.get(username)

# def hash_password(password):
#     hashed_password = hashlib.sha256(password.encode()).hexdigest()
#     return hashed_password

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        response = make_response(redirect(url_for('index')))
        # unset_jwt_cookies(response)
        response.set_cookie('access_token_cookie', expires=datetime.now() - timedelta(days=1))
        return response
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        new_username = request.form['username']
        new_password = request.form['password']
        new_name = request.form['name']
        new_email = request.form['email']
        hashed_password = hash_password(new_password)
        # Save user details to the database or any other storage mechanism if needed
        add_user(new_username,new_email,hashed_password,new_name)
        users=fetch_users()
        return redirect('/')
    return render_template('signup.html')

# @app.route('/login', methods=['POST'])
# def login():
#     data = request.form
#     username = data.get('username')
#     password = data.get('password')

#     if not username or not password:
#         return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

#     if username in users and users[username]['password'] == hash_password(password):
#         access_token = create_access_token(identity=users[username]['user_id'])
#         return jsonify(access_token=access_token), 200
#     else:
#         return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        x = check_user(username,password)

        print(username, hash_password(password))

        if(username=='Admin' and hash_password(password)=='240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9'): #admin password is admin123
            print("addmin")
            access_token = create_access_token(identity=username, expires_delta=timedelta(days=7))
            response = make_response(redirect(url_for('admin')))
            response.set_cookie('access_token_cookie', value=access_token, max_age=3600, httponly=True)
            return response

        if (x==0):
            print('sex')
            return redirect(url_for('signin'))
        user_data = get_user_data(username)
        
        if user_data['password'] == hash_password(password):
            session['user_id'] = username
            session['user_name'] = user_data['name']

            access_token = create_access_token(identity=username, expires_delta=timedelta(days=7))
            response = make_response(redirect(url_for('home', user_id=username)))
            response.set_cookie('access_token_cookie', value=access_token, max_age=3600, httponly=True)
            return response
        else:
            flash('Invalid email or password', 'error')

    flash('Invalid email or password', 'error')

    return render_template('signin.html')


@app.route('/admin', methods=['GET', 'POST'])
@jwt_required()
def admin():
    print('adminussy')
    users=fetch_users();
    db = psycopg2.connect(os.environ["DATABASE_URL"])
    cursor = db.cursor()
    usernames = users.keys()
    for user in usernames:
        query = "SELECT data FROM images WHERE user_id=%s;"
        cursor.execute(query, (users[user]['user_id'],))
        users[user]['images']=cursor.fetchall()
    return render_template('admin.html', usernames=usernames, users=users)

@app.route('/home/<user_id>', methods=['GET', 'POST'])
@jwt_required()
def home(user_id):
    # users = fetch_users()
    # #print(users)
    # current_user = users[get_jwt_identity()]
    # #print(current_user)
    # #print("gaysex")
    # if not current_user:
    #     return redirect(url_for('signin'))
    if session['user_name']!=user_id:
        return redirect(url_for('signin'))
    # if current_user['username']!=user_id:
    #     return redirect(url_for('signin'))
    # response = make_response(redirect(url_for('upload', user_id=current_user['username'])))
    #return response
    return render_template('home.html', user=session['user_id'])
    #return render_template('home.html', user=current_user)

@app.route('/customise', methods=['GET','POST'])
@jwt_required()
def customise():
    print("yayy")
    users = fetch_users()
    #print(users)
    current_user = users[get_jwt_identity()]
    if 'images' not in request.files:
        return 'No image file part in the request', 400
    files = request.files.getlist('images[]')
    print(request.files)
    move_images(current_user['username'], current_user['user_id'],files)

    db = psycopg2.connect(os.environ["DATABASE_URL"])
    cursor = db.cursor()

    images = fetch_images(users[current_user['username']]['user_id'])
    images=[cv2.cvtColor(img, cv2.COLOR_BGR2RGB) for img in images]
    base64_images = [image_to_base64(image) for image in images]
    # print(images)
    return render_template('customise.html', image_list=base64_images)


@app.route('/preview', methods=['GET', 'POST'])
@jwt_required()
def preview():
    users = fetch_users()
    #print(users)
    current_user = users[get_jwt_identity()]
    transitions=[]
    durations=[]
    resolutions=[]

    # Clear previous values
    transitions.clear()
    durations.clear()
    resolutions.clear()

    # Get data from the form
    if request.method=='POST':
        transitions = request.form.getlist('transition')
        durations = [int(i) for i in request.form.getlist('duration')]
        resolution = request.form.get('resolution')
        music_track = request.form.get('music')
    # If duration values are not provided, use default value
    # transition_values = ['fade' if not transition else transition for transition in transition_values]
    # duration_values = [5 if not duration else duration for duration in duration_values]

    # print("kasdfhajghlajkdgkjsghsdlfjkghsjkdfghlfd", request.form)
    # Store transition, duration, and resolution values in lists
    # resolutions.append(resolution_value)

    #MAKE THE VIDEO HERE!!!
    images = fetch_images(users[current_user['username']]['user_id'])
    print(images[0])
    output_file='static/videos/output.mp4'
    background_audio="./yourNewHome.mp3"
    background_audio=f"./static/music/{music_track}.mp3"
    # print("####################################################", resolutions, type(resolution))
    images_to_video(images, output_file, background_audio, transition_list=transitions, duration_list=durations, resolution=int(resolution[:-1]))
    return render_template('preview.html')

@app.route('/download')
def download_video():
    # Path to the video file
    video_path = 'static/videos/output.mp4'
    
    # Serve the file for download
    return send_file(video_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, port="5001")