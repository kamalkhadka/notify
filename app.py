from flask import Flask, render_template, flash, request, redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, User

app = Flask(__name__)

app.config['SECRET_KEY'] = 'chicken1'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///notify'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

debug = DebugToolbarExtension(app)

connect_db(app)

@app.route('/')
def home():
    """ Handle request to root by rendering home page"""
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/users', methods=['POST'])
def users():
    user_json = request.get_json()
    print('****************')
    print(user_json)
    print('****************')
    first_name = user_json.get('first-name')
    last_name = user_json.get('last-name')
    email = user_json.get('email')
    password = user_json.get('password')

    user = User(first_name=first_name, last_name=last_name, email=email, password=password)
    user = User.register(user)
    
    if user:
        print(user)
        flash('User created')
    
    return redirect('/')
    
