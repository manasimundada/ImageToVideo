from flask import Flask, render_template, request, redirect
import hashlib  # Import the hashlib library for password hashing

app = Flask(__name__)

# file_path = "users.txt"

# try:
#     with open(file_path, 'r') as file:
#         profiles = json.load(file)
# except FileNotFoundError:
#     profiles = []
# except json.JSONDecodeError:
#     profiles = []

def hash_password(password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    return hashed_password

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        new_name = request.form['username']
        new_email = request.form['email']
        new_password = request.form['password']

        # hashed_password = hash_password(new_password)

        # new_profile = {'name': new_name, 'email': new_email, 'password': hashed_password}

    return render_template('index.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/signin')
def signin():
    return render_template('signin.html')

@app.route('/home')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)