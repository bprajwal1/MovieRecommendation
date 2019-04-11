from flask import Flask, render_template,request
#from ipynb.fs.full.mr import * 
from mr import *
import sqlite3 as sql
import pandas as pd

app = Flask(__name__)


data = pd.read_csv('movies.csv')

movies_list = data['title'].tolist()
genre_list = data['genres'].tolist()

movies_dict = {}

for i in range(len(movies_list)):
	movies_dict[movies_list[i]] = genre_list[i]

@app.route('/')
def login_page():

	return render_template('login.html')

@app.route('/home_page', methods=['GET','POST'])
def home_page():
	if(request.method == 'POST'):

		uname = request.form['username']
		password = request.form['password']
		print(uname,password)

		#x=genre_recommendation('Adventure') #get genre from database here
		#extract genre here
		con = sql.connect("database.db")
		cur = con.cursor()
		cur.execute("select genre from users where uname=?",(uname,))
		#print(cur.fetchall())
		l=cur.fetchall()[0]
		user_genre_list=[]
		for i in l:
			user_genre_list.append(i)
		user_genre_list=(user_genre_list[0].split(','))
		print(user_genre_list)
		#genre_recommendations('')
		m=''
		for i in movies_dict.keys():
			res = movies_dict.get(i).split('|')
			if(any([i in user_genre_list for i in res])):
				m=i
				break
		print("##################")
		print(m)
		print("###################")
		l=genre_recommendations(m)
		print(l)
		result_list=[]
		for i in l:
			result_list.append(i[:-6])

		con.close()


		return render_template('homepage.html',uname=uname,val=user_genre_list[0],x=result_list)

	else:
		return render_template('homepage.html',uname='Rajesh')

@app.route('/popular_page')
def popular_page():
	'''
	uname = request.form['username']
	password = request.form['password']
	print(uname,password)
	return render_template('homepage.html',uname=uname)
	'''
	return render_template('popular.html',uname='Rajesh')

@app.route('/insert_user',methods =['POST'])
def insert_user():
	uname = request.form['uname']
	email = request.form['email']
	pwd = request.form['psw-repeat']
	genres = request.form.getlist('genre')
	print(uname,email,pwd,genres)
	genre_str = ','.join(genres)
	with sql.connect("database.db") as con:
		print("Connected to database")
		cur = con.cursor()
		cur.execute("INSERT INTO users (uname,emailid,password,genre,recommended,movieID,ratings)  VALUES (?,?,?,?,?,?,?)",(uname,email,pwd,genre_str,'','','') )
		con.commit()
		msg  = 'record inserted successfully'
		print(msg)
	return render_template('login.html')


@app.route('/sign_up')
def sign_up():

	return render_template('signup.html')



if __name__ == '__main__':
	app.run(debug = True)