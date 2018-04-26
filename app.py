from flask import Flask, render_template, request, flash
from iota import *
from time import *
import thread
import time
from flask_login import LoginManager
from flask_security import login_required



from modules import User, sql

app = Flask(__name__)
LoginManager = LoginManager(app)
LoginManager.login_view = "login"

@LoginManager.user_loader
def load_user(userID):
	new_user = User(userID)
	if  new_user.exists():
		return new_user
	else:
		return None

@app.route("/")
def main():
	return render_template('index.html')

@app.route("/sendiota", methods=['GET','POST'])
def sendIota():
	if request.form['submit']:
		_userID = str(request.form['userID'])
		_value = int(request.form['value'])
		_si = request.form['si']

		if _si=='ki':
			_value *= 1e3
		elif _si=='Mi':
			_value *= 1e6

		_time = int(request.form['time'])
		_address = str(request.form['address'])
		_numPayments = int(request.form['numPayments'])

		newUser = User(_userID)
		newUser.setNode("http://node02.iotatoken.nl:14265")
		
		thread.start_new_thread(newUser.iota_send, (_address, _value, _time, _numPayments)) 
		

	return render_template('index.html')

@app.route("/signup",  methods=['GET','POST'])
def userSignup():
	if request.method == 'POST':
		_userID = str(request.form['userID'])
		newUser = User(_userID)
		newUser.setNode("http://node02.iotatoken.nl:14265")
		password = str(request.form['password'])

		passwords_match = (password == str(request.form['confirm']))

		if ((not newUser.exists()) and (passwords_match)):
			_password_hash = newUser.password_encrypt(password)
		
			_email = str(request.form['email'])
			newUser.commitUserToDB(_email, _password_hash)
			newUser.set_is_active(True) #Should wait until email is confirmed in the future, set to 1 in database
			newUser.set_is_anonymous(False)

			next = flask.request.args.get('next')

			if not is_safe_url(next):
				return flask.abort(400)

			return flask.redirect(next or flask.url_for('/signup_success'))

		elif not passwords_match:
			flash("Passwords dont match!")
			return flask.redirect(flask.url_for('/signup'))
		elif newUser(exists) or newUser.db_connection.emailTaken(_email):
			flash("User or Email taken")
			return flask.redirect(flask.url_for('/signup'))

	return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		_userID = str(request.form['userID'])
		_password = str(request.form['password'])
		user = User(_userID)
		if (user.exists and user.password_verify(_password, user.get_password_hash())):
			user.setNode("http://node02.iotatoken.nl:14265")
			user.set_is_authenticated(True)
			
			#Flask login logs in user
			login_user(user)

			next = flask.request.args.get('next')

			if not is_safe_url(next):
				return flask.abort(400)

			return flask.redirect(next or flask.url_for('/yourstats'))

	return render_template('login.html')


@app.route('/yourstats', methods=['GET', 'POST'])
@login_required
def viewStats():
	return render_template('index.html')

@app.route('/signup_success', methods=['GET', 'POST'])
def success():
	return render_template('signup_success.html')


app.secret_key = ""


if __name__ == "__main__":
	app.run()
