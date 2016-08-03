from flask import Blueprint
from flask import Flask, render_template, request, flash, session, redirect, url_for
from .forms import SignupForm, SigninForm, ContactForm
from .model import db, User
from flask_mail import Message, Mail


regular = Blueprint('regular', __name__, template_folder='templates', static_folder='static')
admins = ["admin@phoenixnow.com"]
mail = Mail()


@regular.route('/')
def home():
    return render_template('home.html')

@regular.route('/hello')
def hello():
    """
    Example endpoint

    Returns "hello"
    """
    return "hello"

@regular.route('/signup', methods=['GET', 'POST'])
def signup():

  form = SignupForm()
 
  if 'email' in session:
      return redirect(url_for('.profile'))
  
  if request.method == 'POST':
    if form.validate_on_submit():
      newuser = User(form.firstname.data, form.lastname.data, form.email.data, form.password.data)
      db.session.add(newuser)
      db.session.commit()

      session['email'] = newuser.email
      return redirect(url_for('.profile'))

    else:   
      return render_template('signup.html', form=form)
   
  elif request.method == 'GET':
      return render_template('signup.html', form=form)

@regular.route('/signin', methods=['GET', 'POST'])
def signin():

  form = SigninForm()
 
  if 'email' in session:
      return redirect(url_for('.profile'))
  
  if request.method == 'POST':
    if form.validate_on_submit():
      session['email'] = form.email.data
      return redirect(url_for('.profile'))
    else:
      return render_template('signin.html', form=form)
                 
  elif request.method == 'GET':
    return render_template('signin.html', form=form)

@regular.route('/profile')
def profile():
 
  if 'email' not in session:
    return redirect(url_for('.signin'))

  user = User.query.filter_by(email = session['email']).first()

  if user is None:
    session.pop('email', None)
    return redirect(url_for('.signin'))
  else:
    return render_template('profile.html', user=user)

@regular.route('/signout')
def signout():
 
  if 'email' not in session:
    return redirect(url_for('.signin'))
     
  session.pop('email', None)
  return redirect(url_for('.home'))

@regular.route('/admin')
def admin():
  users = User.query.all()
 
  if session['email'] in admins:
    return render_template('admin.html', users=users)
  else:
    return "unauthorized access"

@regular.route('/contact', methods=['GET','POST'])
def contact():
  form = ContactForm()

  if request.method == 'POST':
    if form.validate_on_submit():
      msg = Message(form.subject.data, sender='support@chadali.me', recipients=['chaudhryam@guilford.edu', form.email.data])
      msg.body = """
      From: %s <%s>
      %s
      """ % (form.name.data, form.email.data, form.message.data)
      mail.send(msg)
      return render_template('contact.html', success=True)
    else:
      flash('All fields are required.')
      return render_template('contact.html', form=form)


  elif request.method == 'GET':
    return render_template('contact.html', form=form)

