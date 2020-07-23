from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(app):
    db.app = app
    db.init_app(app)

class Contact(db.Model):
    """ Model for contacts """
    __tablename__ = 'contacts'
    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    phone = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return f'<Contact: {self.first_name}, {self.last_name}>'

class User(db.Model):
    """ model for users """
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False)
    password = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<User: first_name = {self.first_name}, last_name={self.last_name}>'

    @classmethod
    def authenticate(cls, email, password):
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            return user
        
        return False

    @classmethod
    def register(cls, user):
        user.password = bcrypt.generate_password_hash(user.password)
        db.session.add(user)
        db.session.commit()
        return user

class Template(db.Model):
    __tablename__ = 'templates'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    text = db.Column(db.Text, nullable=False)
    template_type = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return f'<Template: name={self.name}>'


class Message(db.Model):
    
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    message_type = db.Column(db.Boolean, nullable=False, default=0)
    message = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return f'<Message: {self.id} : {self.message}>'


class Group(db.Model):
    
    __tablename__ = 'groups'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'<Group: {self.name}>'


class ContactGroup(db.Model):
    __tablename__ = 'contacts_groups'

    id = db.Column(db.Integer, primary_key=True)
    contact_id = db.Column(db.Integer, db.ForeignKey('contacts.id'))
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'))

    def __repr__(self):
        return f'<ContactGroup: {self.id}>'