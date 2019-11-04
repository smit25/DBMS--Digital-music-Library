# from host import app
# from flask_mysqldb import MySQL 
from flask import Flask,render_template, flash, redirect, request, url_for

import mysql.connector

cur = None
try:
	print("connected")
	connection = mysql.connector.connect(user='root', password='test', host='localhost', database='DBMS')
	print("connected")

	cur = connection.cursor(buffered=True)
	print("connected")
except:
	print("not connected")
app = Flask(__name__,template_folder='template', static_folder='static')
# from flaskext.mysql import MySQL
# mysql = MySQL()

# app.config['MYSQL_DATABASE_USER'] = 'root'
# app.config['MYSQL_DATABASE_PASSWORD'] = '********'
# app.config['MYSQL_DATABASE_DB'] = 'DBMS'
# app.config['MYSQL_DATABASE_HOST'] = 'localhost'

# mysql.init_app(app)
# try:
# 	print("connected")
# 	conn = mysql.connect()
# 	print("connected")
# 	cur =conn.cursor()
# 	print("connected")
# except:
# 	print("not connected")
# app = Flask(__name__,template_folder='template')

# mysql = MySQL(app)
# FOR BASE.HTML
def base():
	# if request.method == 'POST' : 
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
			s_user=cur.execute("SELECT email_id from user as u where u.email_id = '"+email+"';")
			s_user =cur.fetchall()
			if s_user == '' :
				print("Either sign up or enter the correct id")
				return redirect(url_for('signin'))
			s_pass=cur.execute("SELECT password from user as u where u.email_id = '"+email+"';")
			s_pass = cur.fetchall()
			print(Password,s_pass)
			if s_pass[0][0] == Password:
				print("Login Successful")
				cur.execute("SELECT firstname from user as u where u.password = '"+Password+"';")
				f_name=cur.fetchall()
				username=f_name[0][0]
				print("QWERTY",username)
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
	
	login=1
	if request.method == 'POST':
		if 'signup' in request.form:

			User= request.form
			f_name=User(f_name)
			l_name=User(l_name)
			password=User(password)
			email=User(email_id)
			username=f_name
			print("hey")
		# cur=mysql.connection.cursor()
			cur.execute("INSERT INTO user(firstname,lastname,password,email_id) VALUES (%s,%s,%s,%s),(f_name,l_name,password,email);")
			connection.commit()
		# cur.close()
			print("Thank you")

			return redirect(url_for('playlist', username=username))
		else:
			return base()
	else:
		return render_template('signup.html', title ='Sign-Up')

# FOR PLAYLIST OF USER
@app.route('/<username>/playlist', methods =['GET','POST'])
def playlist(username):
	
	print(username)
	check=0
	info=""
	# cur=mysql.connection.cursor()
	cur.execute("SELECT * from playlist where user_id in (SELECT user_id from user as u where u.firstname='"+username+"');")
	playlist=cur.fetchall()
	print(playlist,"QQQQ")
	play_name = ""
	if request.method =='POST':
		if 'play_search' in request.form:
			if request.form['play_search'] == '':
				play_ = request.form['playlist']
				res1 = play_ in (item for sublist in playlist for item in sublist) 
				if  res1==False:
					message = "Playlist not found"
					return redirect(url_for('playlist',username = username, message = message))
				else:
					return redirect(url_for('songs',play_name = play_, username = username))
			if request.form['play_search'] == 'I':
				check=1
				title_info=request.form['play_search']
				# cur=mysql.connection.cursor()
				cur.execute("SELECT info from playlist where playlist.title = '"+title_info+"';")
				info = cur.fetchall()
		elif 'create_playlist' in request.form:
			print(username,"test_u")
			return redirect(url_for('createplaylist', username=username))
		else:
			return base()

	else:
		return render_template('playlist.html', title='Playlists', playlist = play_name, check=check, info=info,username=username)

check=0
# FOR CREATING A NEW PLAYLIST
@app.route('/<username>/createplaylist', methods = ['GET','POST'])
def createplaylist(username):
	message=""
	if request.method == 'POST':
		if 'create_p' in request.form:
			playlist=request.form
			title=playlist['Title']
			print(title)
			Info=playlist['Info']
			print(Info)
			cur.execute("SELECT user_id from user as u where u.firstname= '"+username+"';")
			user_id=cur.fetchall()
			print(user_id[0][0],username)
			# cur=mysql.connection.cursor()
			cur.execute("INSERT INTO playlist(title,info,user_id) VALUES ('"+title+"','"+Info+"',"+str(user_id[0][0])+");")
			connection.commit()
			# cur.close()
			message = "Thank you"
			return redirect('/<username>/playlist')
		
			return base()
	else:
		return render_template('createplaylist.html', title = 'Create Playlist', username=username, message = message)

# FOR ADDING SONGS TO THE PLAYLIST

@app.route('/<username>/<play_name>', methods =['GET','POST']) 
def songs(username,play_name):
	# cur=mysql.connection.cursor()
	cur.execute("SELECT * from songs where playlist_id in (SELECT playlist_id from playlist where playlist.title = '"+play_name+"');")
	songss=cur.fetchall()

	# cur.close()
	if request.method == 'POST':
		if 'delete' in request.form:
			Delete_s= request.form
			song_tobedeleted = Delete_s['delete']				# cur=mysql.connection.cursor()
			cur.execute("DELETE from songs where songs.title = '"+song_tobedeleted+"';")
			connection.commit()
				# cur.close()
		if 'upload_songs' in request.form:
			return redirect(url_for('upload',username=username, play_name=play_name))

		if 'song_info' in request.form:
			song_name=request.form
			# cur=mysql.connection.cursor()
			cur.execute("SELECT info from songs where title='"+song_name+"';")
			info=cur.fetchall()
				# cur.close()
		elif 'user_info' in request.form:
			song_name=request.form
			cur.execute("SELECT playlist_id from songs where songs.title = '"+song_name+"');")
			playlist_id=cur.fetchall()
			# cur=mysql.connection.cursor()
			cur.execute("SELECT firstname,lastname, email_id from user INNER JOIN playlist on user.user_id = playlist.user_id INNER JOIN songs on playlist.play_id = songs.playlist_id where songs.playlist_id = '"+playlist_id[0][0]+"';")
			info=cur.fetchall()
				# cur.close()
		elif 'playlist_info' in request.form:
			song_name=request.form
			cur.execute("SELECT playlist_id from songs where songs.title = '"+song_name+"');")
			playlist_id=cur.fetchall()
			cur.execute("SELECT info from playlist where playlist_id = '"+playlist_id[0][0]+"';")
			info=cur.fetchall()

		elif 'comment' in request.form:
			song_name=request.form
			return redirect(url_for('comment'), song_name = song_name,songss=songss, username = username, play_name = play_name)
       
       
		else:
			return base()		
				
	else:
		return render_template('songs.html', title ='<play_name>',songss=songss, play_name = play_name, username=username)


# FOR UPLOAIDNG SONGS
@app.route('/<username>/<play_name>/upload', methods = ['GET','POST'])
def upload(username,play_name):
	if request.method == 'POST':
		if 'upload' in request.form:
			song_u=request.form
			title=song_u['Title']
			Info=song_u['Info']
			link=song_u['link']
			cate=song_u['category']
			cur.execute("SELECT category_id from category where category.text = '"+cate+"';")
			category_id=cur.fetchall()
			print(category_id,"cat")
			cur.execute("SELECT playlist_id from playlist where playlist.title = '"+play_name+"';")
			playlist_id=cur.fetchall()
			print(playlist_id,"play")
			# cur=mysql.connection.cursor()
			cur.execute("INSERT INTO songs(title,link,info,playlist_id,category_id) VALUES ('"+title+"','"+link+"','"+Info+"','"+str(playlist_id[0][0])+"','"+str(category_id[0][0])+"');")
			connection.commit()
		# cur.close()
			print("Thank you")
			cur.execute("SELECT * from songs where playlist_id = '"+playlist_id+"';")
			songss=cur.fetchall()
			print(songss)

			return redirect(url_for('songs', username=username, play_name = play_name,songss=songss) )
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
				cur.execute(" UPDATE user set user.subscription = user.subscription +1 where user.f_name = '"+user_s+"' ;")
				connection.commit()
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
				cur.execute("SELECT user_id from user where user.firstname='"+username+"';")
				user_id = cur.fetchall()
				cur.execute("INSERT INTO comments(text_c,song_id,user_id) VALUES ('"+com+"','"+song_name+"','"+user_id[0][0]+"');")
				connection.commit()


			elif request.form['comment'] == 'view_com_s':
				check =1
				cur.execute("SELECT song_id from songs where songs.title='"+song_name+"';")
				Song_id=cur.fetchall()
				cur.execute("SELECT text_c from comments where song_id = '"+Song_id+"';")
				view_com=cur.fetchall()

			elif request.form['comment'] == 'view_com_u':
				check =2
				cur.execute("SELECT user_id from user where user.firstname='"+username+"';")
				user_id = cur.fetchall()
				cur.execute("SELECT text_c from comments where user_id = '"+user_id[0][0]+"';")
				view_com=cur.fetchall()
		else:
			return base()
	else:
		return render_template('comment.html', title = '<username>/<song_name>/comment',com=com, view_com = view_com,check=check)

# FOR SEGREGATING THE SONGS INTO CATEGORIES
@app.route('/category', methods = ['GET','POST'])
def category():
	# base()
	cur.execute(" SELECT text from category ")
	types=cur.fetchall()
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
		cur.execute("SELECT songs.title from songs where songs.category_id in (SELECT category_id from category where category.text='"+s+"');")
		song_cat = cur.fetchall()
		cur.execute("SELECT songs.link from songs where songs.category_id in (SELECT category_id from category where category.text='"+s+"');")
		song_link = cur.fetchall()
		return render_template('category_songs.html', s=s, song_cat = song_cat, song_link = song_link)

# cur.close()
if __name__ == '__main__':
    app.run(debug=True)


