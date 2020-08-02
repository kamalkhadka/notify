from flask import Flask, render_template, flash, request, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, User, Contact, Group, db, EmailLimit
from forms import SignupForm, LoginForm, ContactForm, GroupForm, MessageForm, VerifyUserForm
import os
import requests
from datetime import date

app = Flask(__name__)

app.config['SECRET_KEY'] = 'chicken1'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///notify'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

sendgrid_key = os.environ.get('SENDGRID_API_KEY')
authy_key = os.environ.get('AUTHY_API_KEY')

debug = DebugToolbarExtension(app)

connect_db(app)


def check_email_limit():
    email_limit = EmailLimit.query.get(1)
    if email_limit and email_limit.date.date() == date.today():
        count = email_limit.count
        if count < 100:
            return True
        else:
            flash('Message limit reached for today')
            return False

    if email_limit and email_limit.date.date() < date.today():
        email_limit.count = 0
        return True

    if not email_limit:
        email_limit = EmailLimit(date=date.today())
        EmailLimit.create(email_limit)
        if email_limit:
            return True

    # return False


@app.route('/')
def home():
    """ Handle request to root by rendering home page"""
    user_id = session.get('user_id', False)
    if user_id:
        return redirect(f'/users/{user_id}')
    else:
        return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.authenticate(email=email, password=password)
        if user and check_email_limit():
            session['user_id'] = user.id
            return redirect(f'/users/{user.id}')
        else:
            flash('Login failed')
            return redirect('/login')
    else:
        return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    session.pop('user_id')
    flash('Logged out')
    return redirect('/')


@app.route('/signup', methods=['GET', 'POST'])
def users():
    signup_form = SignupForm()
    if signup_form.validate_on_submit():
        first_name = signup_form.first_name.data
        last_name = signup_form.last_name.data
        email = signup_form.email.data
        password = signup_form.password.data
        phone = signup_form.phone.data

        authy_id = create_authy_user(email, phone)

        if authy_id and check_email_limit() and send_otp_email(authy_id):
            EmailLimit.increase_count(EmailLimit.query.get(1))

        user = User(first_name=first_name, last_name=last_name,
                    email=email, password=password, phone=phone, authy_id=authy_id)

        user = User.register(user)

        flash('User created. Please login')
        return redirect('/')
    else:
        return render_template('signup.html', form=signup_form)


@app.route('/users/<int:id>')
def get_user(id):
    user = check_user_session(id)
    if not user:
        return redirect('/')
    return render_template('/users/index.html', user=user)


@app.route('/users/<int:id>/contacts/create', methods=['GET', 'POST'])
def create_contact(id):
    user = check_user_session(id)
    if not user:
        return redirect('/')
    contact_form = ContactForm()
    if contact_form.validate_on_submit():
        first_name = contact_form.first_name.data
        last_name = contact_form.last_name.data
        email = contact_form.email.data

        contact = Contact(first_name=first_name, last_name=last_name,
                          email=email, user_id=user.id)
        contact = Contact.create_contact(contact)
        return redirect(f'/users/{user.id}')
    else:
        return render_template('/users/contact.html', form=contact_form, user=user)


@app.route('/users/<int:id>/groups/create', methods=['GET', 'POST'])
def create_group(id):
    user = check_user_session(id)
    if not user:
        return redirect('/')

    group_form = GroupForm()
    if group_form.validate_on_submit():
        name = group_form.name.data
        group = Group(name=name, user_id=user.id)
        group = Group.create_group(group)
        flash(f'Group created: {name}')
        return redirect(f'/users/{user.id}')
    else:
        return render_template('/users/group.html', form=group_form, user=user)


@app.route('/groups/<int:group_id>')
def edit_group(group_id):
    group = Group.query.get_or_404(group_id)
    user = check_user_session(group.user_id)
    if not user:
        flash('Unauthorized access')
        return redirect('/')
    return render_template('/users/groups/index.html', group=group)


@app.route('/groups/<int:group_id>/delete')
def delete_group(group_id):
    group = Group.query.get_or_404(group_id)
    user = check_user_session(group.user_id)
    if not user:
        flash('Unauthorized access')
        return redirect('/')
    if Group.delete_group(group) and not Group.query.get(group_id):
        flash(f'Group {group.name} deleted')
        return redirect('/')


@app.route('/groups/<int:id>/contacts/add', methods=['GET', 'POST'])
def add_contact_to_group(id):
    group = Group.query.get_or_404(id)
    user = check_user_session(group.user_id)
    if not user:
        flash('Unauthorized access')
        return redirect('/')
    elif request.method == 'GET':
        contacts = Group.get_contacts_not_in_group(group.id)
        return render_template('/users/contacts/add-contact.html', contacts=contacts, group=group)
    else:
        contacts = group.contacts

        for value in request.form.to_dict():
            contacts.append(Contact.query.get(int(value)))
        db.session.commit()

        return redirect(f'/groups/{group.id}')


@app.route('/groups/<int:id>/messages', methods=['GET', 'POST'])
def send_group_message(id):
    group = Group.query.get_or_404(id)

    user = check_user_session(group.user_id)
    if not user:
        flash('Unauthorized access')
        return redirect('/')

    form = MessageForm()

    if form.validate_on_submit():
        message = form.message.data
        subject = form.subject.data
        emails = [contact.email for contact in group.contacts]

        # if sendgrid_status in [200, 202]:
        for email in emails:
            send_message(to_email=email, message=message,
                         user=group.user, subject=subject)
        flash(f'Message sent to {group.name}')
        # elif sendgrid_status == 429:
        # flash(f'Limit exceeded for today')

        return redirect('/')
    else:
        return render_template('/users/groups/send-group-message.html', form=form, group=group)


@app.route('/contacts/<int:id>/messages', methods=['GET', 'POST'])
def send_message_to_contact(id):
    contact = Contact.query.get_or_404(id)
    user = check_user_session(contact.user_id)
    if not user:
        flash('Unauthorized access')
        return redirect('/')

    form = MessageForm()

    if form.validate_on_submit():
        message = form.message.data
        subject = form.subject.data
        email = contact.email

        send_message(to_email=email, message=message,
                     user=user, subject=subject)
        flash(f'Message sent to {contact.first_name} {contact.last_name}')

        return redirect('/')
    else:
        return render_template('/users/contacts/send-message.html', form=form, contact=contact)


@app.route('/contacts/<int:contact_id>/edit', methods=['GET', 'POST'])
def edit_contact(contact_id):
    contact = Contact.query.get_or_404(contact_id)
    user = check_user_session(contact.user_id)
    if not user:
        flash('Unauthorized request')
        return redirect('/')

    contact_form = ContactForm(obj=contact)
    if contact_form.validate_on_submit():
        contact.first_name = contact_form.first_name.data
        contact.last_name = contact_form.last_name.data
        contact.email = contact_form.email.data
        Contact.update_contact(contact)
        flash(f'Updated {contact.first_name}.')
        return redirect('/')
    else:
        return render_template('/users/contacts/edit-contact.html', form=contact_form, contact=contact)


@app.route('/contacts/<int:contact_id>/delete')
def delete_contact(contact_id):
    contact = Contact.query.get_or_404(contact_id)
    user = check_user_session(contact.user_id)
    if not user:
        flash('Unauthorized request')
        return redirect('/')

    if Contact.delete_contact(contact):
        flash(f'{contact.first_name} deleted.')
        return redirect('/')
    else:
        flash(f'Something went wrong while deleting {contact.first_name}.')
        return redirect('/')


@app.route('/groups/<int:group_id>/contacts/<int:contact_id>/remove', methods=['GET'])
def remove_contact_from_group(group_id, contact_id):
    group = Group.query.get_or_404(group_id)
    contact = Contact.query.get_or_404(contact_id)
    Group.remove_contact(group, contact)
    flash(f'Contact: {contact.first_name} removed from {group.name}')
    return redirect(f'/groups/{group.id}')


@app.route('/users/<int:user_id>/verify', methods=['GET', 'POST'])
def verify_token(user_id):
    user = check_user_session(user_id)
    if not user:
        flash('Unauthorized request')
        return redirect('/')

    verify_user_form = VerifyUserForm()
    if verify_user_form.validate_on_submit():
        token = verify_user_form.token.data
        if check_token(token, user.authy_id):
            user.is_valid = True
            db.session.commit()
            return redirect('/')
        else:
            flash(f'Not a valid token. Click Resend Token to get a new token')
            return redirect(f'/users/{user.id}/verify')

    return render_template('/users/verify.html', form=verify_user_form, user=user)


@app.route('/users/<int:user_id>/resend')
def resend_token(user_id):
    user = check_user_session(user_id)
    if not user:
        flash('Unauthorized request')
        return redirect('/')

    if send_otp_email(user.authy_id):
        flash('Verification email sent.')
        return redirect('/')
    else:
        flash('Not sure what went wrong.')
        return redirect('/')
    

def check_user_session(id):
    user = User.query.get_or_404(id)
    user_id = session.get('user_id', False)

    if not user_id:
        return False
    elif user.id != user_id:
        return False
    else:
        return user


def send_message(to_email, message, user, subject):
    url = "https://api.sendgrid.com/v3/mail/send"

    payload = {
        "personalizations": [
            {
                "to": [
                    {
                        "email": to_email
                    }
                ],
                "subject": subject
            }
        ],
        "from": {
            "email": "wikidi9678@lege4h.com"
        },
        "content": [
            {
                "type": "text/html",
                "value": message
            }
        ],
        "reply_to": {"email": user.email, "name": user.first_name + " " + user.last_name}
    }

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {sendgrid_key}'
    }

    if not check_email_limit():
        email_limit.count = 100
        email_limit = EmailLimit.query.get(1)
        EmailLimit.reset_count(email_limit)

    EmailLimit.increase_count(EmailLimit.query.get(1))
    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 201:
        EmailLimit.increase_count(EmailLimit.query.get(1))
    elif response.status_code in [400, 429, 500]:
        flash(f'Email limit reached check back tomorrow')
        email_limit = EmailLimit.query.get(1)
        email_limit.count = 100
        EmailLimit.reset_count(email_limit)


authy_base_url = 'https://api.authy.com'


def create_authy_user(email, phone):
    payload = {
        "user": {
            "email": email,
            "cellphone": phone,
            "country_code": 1
        }

    }

    headers = {
        "X-Authy-API-Key": authy_key
    }

    response = requests.post(
        authy_base_url + '/protected/json/users/new', headers=headers, json=payload)
    json = response.json()
    print(json)
    return json['user']['id']


def send_otp_email(authy_id):
    headers = {
        'X-Authy-API-Key': authy_key
    }
    response = requests.post(
        authy_base_url+f'/protected/json/email/{authy_id}', headers=headers)
    json = response.json()

    if json['success']:
        return True
    else:
        return False


def check_token(token, authy_id):
    headers = {
        'X-Authy-API-Key': authy_key
    }
    response = requests.get(
        authy_base_url+f'/protected/json/verify/{token}/{authy_id}', headers=headers)
    json = response.json()
    if json['success']:
        return True
    else:
        return False
