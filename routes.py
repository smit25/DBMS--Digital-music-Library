# from host import app
from flask import Flask,render_template, flash, redirect, request, url_for
# from flask_mysqldb import MySQL 
"""
import mysql.connector
# from datetime import datetime
cur = None
try:
	connection = mysql.connector.connect(user='root', password='NO', host='localhost', database='DBMS')
	cur = connection.cursor()
	print("connected")
except:
	print("not connected")
"""
from flask import Flask
from flaskext.mysql import MySQL
mysql = MySQL()
app = Flask(__name__,template_folder='template')
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'impact25'
app.config['MYSQL_DATABASE_DB'] = 'DBMS'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
try:
	conn = mysql.connect()
	cur =conn.cursor()
	print("connected")
except:
	print("not connected")
# app = Flask(__name__,template_folder='template')

# mysql = MySQL(app)
# FOR BASE.HTML
def base():
	print(request.form['nav'])
	if request.method == 'POST' : 
		if request.form['nav'] == 'login':
			print("I'm going back :)\n")
			return redirect(url_for('login'))
		if request.form['nav'] == 'category':
			return redirect(url_for('category'))
		else:
			# print("I'm going back :/\n")
			return redirect(url_for('index'))

@app.route('/',methods=['POST','GET'])
# FOR HOMEPAGE
@app.route('/home',methods =['POST','GET'])
def index():
	if request.method == 'POST': 
		if 'login' in request.form:
			if request.form['login'] == 'I':
				return redirect(url_for('login'))
		else :
			return base()
	else :
		return render_template('home.html', title = 'Home')

	# LOGIN
@app.route('/login',methods = ['GET','POST'])
def login():
	# base()
	if request.method == 'POST':
		if 'sign' in request.form:
			if request.form['sign'] == 'signin':
				return redirect(url_for('signin'))
			if request.form['sign'] == 'signup':
				return redirect(url_for('signup'))
		else:
			return base()
	else:
		return render_template('login.html', title = 'Login')

login =0
# FOR SIGNIN
@app.route('/login/signin', methods = ['GET','POST'])
def signin():
	# base(request)
	if request.method == 'POST':
		if 'signin' in request.form:
			User = request.form
			email = User['email']
			Password = User['password']
			# cur=mysql.connection.cursor()
			s_user=cur.execute("SELECT email_id from user as u where u.email_id = 'email'")
			if s_user ==  NULL:
				print("Either sign up or enter the correct id")
				return redirect(url_for('signin'))
			sss_pass=cur.execute("SELECT password from user as u where u.email_id = 'email'")
			if s_pass == Password:
				print("Login Successful")
				f_name=cur.execute("SELECT firstname from user as u where u.password = 's_pass'")
				username=f_name
				login=1
				return redirect(url_for('playlist', username=username))
			else:
				print("Enter the correct password!")
				return redirect(url_for('signin'))
		else:
			return base()
		# cur.close()
	else:
		return render_template('signin.html', title = 'Sign-in')


# FOR SIGNUP
@app.route('/login/signup', methods = ['GET','POST'])
def signup():
	
	error = False
	login=1
	if request.method == 'POST':
		if 'signup' in request.form:

			User= request.form
			f_name=User(f_name)
			l_name=User(l_name)
			password=User(password)
			email=User(email_id)
			username=f_name

		# cur=mysql.connection.cursor()
			cur.execute("INSERT INTO user(firstname,lastname,password,email_id) VALUES (%s,%s,%s,%s)",(f_name,l_name,password,email))
			connection.commit()
		# cur.close()
			print("Thank you")

			return redirect(url_for('playlist', username=username))
		else:
			return base()
	else:
		return render_template('signup.html', title ='Sign-Up', error = error)

# FOR PLAYLIST OF USER
@app.route('/<username>/playlist', methods =['GET','POST'])
def playlist(username):
	
	check=0
	info=""
	# cur=mysql.connection.cursor()
	playlist =cur.execute("SELECT * from playlist where user_id in (SELECT user_id from user as u where u.firstname='username')")
	play_name = ""
	if request.method =='POST':
		if 'play_search' in request.form:
			if request.form['play_search'] == '':
				play = request.form['play_search']
				play_name= play(playlist)
				if play_name not in playlist[title]:
					message = "Playlist not found"
					return redirect(url_for('playlist',username = username, message = message))
				else:
					return redirect(url_for('songs',play_name = play_name, username = username))
			if request.form['play_search'] == 'I':
				check=1
				title_info=request.form['play_search']
				# cur=mysql.connection.cursor()
				info=cur.execute("SELECT info from playlist where playlist.title = 'title_info'")
			# cur.close()
		else:
			return base()

	else:
		return render_template('playlist.html', title='Playlists', playlist = play_name, check=check, info=info,username=username)

check=0
# FOR CREATING A NEW PLAYLIST
@app.route('/<username>/createplaylist', methods = ['GET','POST'])
def createplaylist(username):

	if request.method == 'POST':
		if 'create_p' in request.form:
			playlist=form.request
			title=playlist['Title']
			Info=playlist['Info']
			# cur=mysql.connection.cursor()
			cur.execute("INSERT INTO playlist(title,info,user_id) VALUES (%s,%s,%d),(title, Info,user_id) where user_id in (SELECT user_id from user as u where u.firstname= 'username')")
			connection.commit()
			# cur.close()
			message = "Thank you"
			return redirect('/<username>/playlist', username=username)
		else:
			return base()
	else:
		return render_template('createplaylist.html', title = 'Create Playlist', username=username, message = message)

# FOR ADDING SONGS TO THE PLAYLIST

@app.route('/<username>/<play_name>', methods =['GET','POST']) 
def songs(username,play_name):
	# cur=mysql.connection.cursor()
	songs=cur.execute("SELECT * from songs where playlist_id in (SELECT playlist_id from playlist where playlist.title = 'play_name')")
	# cur.close()
	if request.method == 'POST':
		if 'delete' in request.form:
			Delete_s= form.request
			song_tobedeleted = Delete_s['delete']				# cur=mysql.connection.cursor()
			songs=cur.execute("DELETE from songs where song.title = 'song_tobedeleted'")
				# cur.close()
	
		if 'song_info' in request.form:
			song_name=request.form
			# cur=mysql.connection.cursor()
			info=cur.execute("SELECT info from songs where song.title=song_name")
				# cur.close()
		elif 'user_info' in request.form:
			song_name=request.form
			# cur=mysql.connection.cursor()
			info=cur.execute("SELECT firstname,lastname, email_id from user INNER JOIN playlist on user.user_id = playlist.user_id INNER JOIN songs on playlist.play_id = songs.playlist_id where songs.playlist_id in(SELECT playlist_id from songs where songs.title = 'song_name'")
				# cur.close()
		elif 'playlist_info' in request.form:
			song_name=request.form
			info=cur.execute("SELECT info from playlist where playlist_id in ( SELECT playlist_id from songs where songs.title = 'song_name')")

		elif 'comment' in request.form:
			song_name=request.form
			return redirect(url_for('comment'), song_name = song_name, username = username, play_name = play_name)
       
       
		else:
			return base()		# cur=mysql.connection.cursor()
				# cur.close()
	else:
		return render_template('songs.html', title ='<play_name>',songs=songs, play_name = play_name, info=info, username=username)


# FOR UPLOAIDNG SONGS
@app.route('/<username>/<play_name>/upload', methods = ['GET','POST'])
def upload(username,play_name):
	if request.method == 'POST':
		if 'upload' in request.form:
			song_u=form.request
			title=song_u['Title']
			Info=song_u['Info']
			link=song_u['link']
			cate=song_u['category']
			# cur=mysql.connection.cursor()
			cur.execute("INSERT INTO songs(title,link,info,playlist_id,category_id) VALUES (%s,%s,%s,%d,%d), (title,link,Info,playlist_id,category_id) where playlist_id in (SELECT playlist_id from playlist where playlist.title = 'play_name') and category_id in (SELECT category_id from category where category.text = 'cate')")
			connection.commit()
		# cur.close()
			print("Thank you")
			return rediect(url_for('songs', username=username, play_name = play_name,) )
		else:
			return base()
	else:
		return render_template('upload.html', title = 'upload', username=username,  play_name = play_name)


# FOR SUBSCRIBING TO A USER
app.route('/subscribe', methods = ['GET','POST'])
def subscribe(username):
	message =""
	if request.method == 'POST':
		if 'subscribe' in request.form:
			user_s=request.form['user_s']
			if user_s != "":
				cur.execute(" UPDATE user set user.subscription = user.subscription +1 where user.f_name = 'user_s' ")
				message= "Thank You for subscribing"
			else:
				message = " Please type the name of the user you want to subscribe"
		else:
			return base()
	else:
		return render_template('subscribe.html', title ='subscribe', message = message)

app.route('/<username>/<song_name>/comment', methods = ['GET','POST'])

# FOR COMMENTING ON A SONG
def comment(username, play_name,song_name):
	check = 0
	if request.method == 'POST':
		if 'comment' in request.form:
			if request.form['comment'] == 'enter_comment':
				com=request.form['comment']
				cur.execute("INSERT INTO comments(text_c,song_id,user_id) VALUES(%s,%d,%d), (com,song_name,user_id) where user_id in( SELECT user_id in user where user.firstname = 'username')")
				connection.commit()


			elif request.form['comment'] == 'view_com_s':
				check =1
				view_com=cur.execute("SELECT text_c from comments where song_id in (SELECT song_id from songs where songs.title='song_name')")

			elif request.form['comment'] == 'view_com_u':
				check =2
				view_com=cur.execute("SELECT text_c from comments where user_id in (SELECT user_id from user where user.firstname='username')")
		else:
			return base()
	else:
		return render_template('comment.html', title = '<username>/<song_name>/comment',com=com, view_com = view_com,check=check)

# FOR SEGREGATING THE SONGS INTO CATEGORIES
@app.route('/category', methods = ['GET','POST'])
def category():
	# base()
	types = cur.execute(" SELECT text from category ")
	if request.method == 'POST':
		if 'category' in request.form:
			s = request.form['category']
	
			return redirect(url_for('category_songs', s=s))
		else:
			return base()
	else:
		return render_template('category.html', title = 'category', types = types)

# FOR DISPLAYING THE SONGS IN CATEGORY
@app.route('/category/songs', methods =['GET','POST'])
def category_songs(s):
	if request.method =='POST':
		return base()
	else:
		song_cat = cur.execute("SELECT songs.title from songs where songs.category_id in (SELECT category_id from category where category.text='s')")
		song_link = cur.execute("SELECT songs.link from songs where songs.category_id in (SELECT category_id from category where category.text='s')")
		return render_template('category_songs.html', s=s, song_cat = song_cat, song_link = song_link)

# cur.close()
if __name__ == '__main__':
    app.run(debug=True)


