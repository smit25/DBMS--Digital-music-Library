# from host import app
from flask import Flask,render_template, flash, redirect, request, url_for
# from flask_mysqldb import MySQL 
import mysql.connector

try:
    connection = mysql.connector.connect(user='root', password='impact25', host='localhost', database='DBMS')
    cur = connection.cursor()
    print("connected")
except:
    print("not connected")

app = Flask(__name__,template_folder='template')

# mysql = MySQL(app)
@app.route('/',methods=['POST','GET'])
def base():
	if request.method == 'POST' and request.form['nav'] == 'login':
		return redirect(url_for('login'))
	if request.method == 'POST' and request.form['nav'] == 'subscribe':
		return redirect(url_for('subscribe'))
	if request.method == 'POST' and request.form['nav'] == 'category':
		return redirect(url_for('category'))
	else:
		return redirect(url_for('index'))
@app.route('/home',methods =['POST','GET'])
def index():
	if request.method == 'POST':
		return redirect(url_for('login'))
	return render_template('home.html', title = 'Home')
@app.route('/login',methods = ['GET','POST'])
def login():
	if request.method == 'POST' and request.form['sign'] == 'signin':
		return redirect(url_for('signin'))
	if request.method == 'POST' and request.form['sign'] == 'signup':
		return redirect(url_for('signup'))
	return render_template('login.html', title = 'Login')

login =0
@app.route('/login/signin', methods = ['GET','POST'])
def signin():
	if request.method == 'POST':
		User = request.form
		email = User['email']
		Password = User['password']
		# cur=mysql.connection.cursor()
		s_user=cur.execute("SELECT email_id from user as u where u.email_id = 'email'")
		if s_user ==  NULL:
			print("Either sign up or enter the correct id")
		s_pass=cur.execute("SELECT password from user as u where u.email_id = 'email'")
		if s_pass == Password:
			print("Login Successful")
			f_name=cur.execute("SELECT firstname from user as u where u.password = 's_pass'")
			username=f_name
			login=1
			return redirect(url_for('playlist', username=username))
		else:
			print("Enter the correct password!")
		# cur.close()
	return render_template('signin.html', title = 'Sign-in')

@app.route('/login/signup', methods = ['GET','POST'])
def signup():
	error = False
	login=1
	if request.method == 'POST':
		User= request.form
		f_name=User(f_name)
		l_name=User(l_name)
		password=User(password)
		email=User(email_id)
		username=f_name

		# cur=mysql.connection.cursor()
		cur.execute("INSERT INTO user(firstname,lastname,password,email_id) VALUES (%s,%s,%s,%s)",(f_name,l_name,password,email))
		mysql.connection.commit()
		# cur.close()
		print("Thank you")

		return redirect(url_for('playlist', username=username))
	return render_template('signup.html', title ='Sign-Up', error = error)
@app.route('/<username>/playlist', methods =['GET','POST'])
def playlist(username):
	check=0
	# cur=mysql.connection.cursor()
	playlist =("SELECT * from playlist where user_id in (SELECT user_id from user as u where u.firstname='username')")
	# cur.close()
	if request.method =='POST':
		if request.form['Search'] == '':
			play = request.form['Search']
			play_name= play(playlist)
			if play_name not in playlist[title]:
				print("Playlist not found")
				return redirect('/<username>/playlist')
			else:
				return redirect(url_for('songs',play_name = play_name))
		else:
			check=1
			title_info=request.form['Search']
			# cur=mysql.connection.cursor()
			info=("SELECT info from playlist where playlist.title = 'title_info'")
			# cur.close()


	return render_template('playlist.html', title='Playlists', playlist = play_name, check=check, info=info,username=username)

check=0

@app.route('/<username>/createplaylist', methods = ['GET','POST'])
def createplaylist(username):
	if request.method == 'POST':
		playlist=form.request
		title=playlist['Title']
		Info=playlist['Info']
		# cur=mysql.connection.cursor()
		cur.execute("INSERT INTO playlist(title,info,user_id) VALUES (%s,%s,%d),(title, Info,user_id) where user_id in (SELECT user_id from user as u where u.firstname= 'username')")
		mysql.connection.commit()
		# cur.close()
		print("Thank you")

	return redirect('/<username>/playlist', username=username)
	return render_template('createplaylist.html', title = 'Create Playlist', username=username)

@app.route('/<username>/<play_name>', methods =['GET','POST']) 
def songs(username,play_name):
	# cur=mysql.connection.cursor()
	songs=cur.execute("SELECT * from songs where playlist_id in (SELECT playlist_id from playlist where playlist.title = 'play_name')")
	# cur.close()
	def delete():
		if request.method == 'POST':
			if 'delete' in request.form:
				Delete_s= form.request
				song_tobedeleted = Delete_s['delete']
				# cur=mysql.connection.cursor()
				songs=cur.execute("DELETE from songs where song.title = 'song_tobedeleted'")
				# cur.close()
	def req_info():
		if 'song_info' in request.form:
			if request.method == 'POST':
				song_name=request.form
				# cur=mysql.connection.cursor()
				info=cur.execute("SELECT info from songs where song.title=song_name")
				# cur.close()
		elif 'user_info' in request.form:
			if request.method == 'POST':
				song_name=request.form
				# cur=mysql.connection.cursor()
				info=cur.execute("")
				# cur.close()
		elif 'playlist_info' in request.form:
			if request.method == 'POST':
				song_name=request.form
				info=cur.execute("SELECT info from playlist where playlist_id in ( SELECT playlist_id from songs where songs.title = 'song_name')")

		elif 'comment' in request.form:
			if request.method == 'POST':
				song_name=request.form
				return redirect(url_for('comment'), song_name = song_name, username = username, play_name = play_name)
       
       
				# cur=mysql.connection.cursor()
				# cur.close()
    	
	return render_template('songs.html', title = '<play_name>', songs=songs, play_name = play_name, info=info, username=username)

@app.route('/<username>/<play_name>/upload', methods = ['GET','POST'])
def upload(username,play_name):
	if request.method == 'POST':
		song_u=form.request
		title=song_u['Title']
		Info=song_u['Info']
		link=song_u['link']
		# cur=mysql.connection.cursor()
		cur.execute("INSERT INTO songs(title,link,info,playlist_id) VALUES (%s,%s,%s,%d), (title,link,Info,playlist_id) where playlist_id in (SELECT playlist_id from playlist where playlist.title = 'play_name'")
		mysql.connection.commit()
		# cur.close()
		print("Thank you")
	return rediect('/<username>/<play_name>', username=username, play_name = play_name,)
	return render_template('upload.html', title = 'upload', username=username,  play_name = play_name)

app.route('/subscribe', methods = ['GET','POST'])
def subscribe(username):
	if request.method == 'POST':
		user_s=request.form['user_s']

		cur.execute(" UPDATE user set user.subscription = user.subscription +1 where user.f_name = 'user_s' ")
		message= "Thank You for subscribing"
	else:
		message = " Please type the name of the user you want to subscribe"
	return render_template('subscribe.html', title ='subscribe', message = message)

app.route('/<username>/<song_name>/comment', methods = ['GET','POST'])
def comment(username, play_name,song_name):
	check = 0
	if request.method == 'POST' and request.form['comment'] == 'enter_comment':
		com=request.form['comment']
		cur.execute("INSERT INTO comments(text_c,song_id,user_id) VALUES(%s,%d), (com,song_name,user_id) where user_id in( SELECT user_id in user where user.firstname = 'username')")

	elif request.method == 'POST' and request.form['comment'] == 'view_com_s':
		check =1
		view_com=cur.execute("SELECT text_c from comments where song_id in (SELECT song_id from songs where songs.title='song_name')")

	elif request.method == 'POST' and request.form['comment'] == 'view_com_u':
		check =2
		view_com=cur.execute("SELECT text_c from comments where user_id in (SELECT user_id from user where user.firstname='username')")

	return render_template('comment.html', title = '<username>/<song_name>/comment',com=com, view_com = view_com,check=check)


# cur.close()
if __name__ == '__main__':
    app.run(debug=True)


