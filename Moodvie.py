

###########################################
# All the imports
from flask import Flask, request, session, redirect, url_for, render_template, flash
app = Flask(__name__)
import os


###########################################
def dictMoodvies(fileName):
    fin = open(fileName) 
    moodvies = []
    dictMoodvies = dict()     
    for line in fin:
        line = line.strip()
        moodvies.append(line.split(', ')) 
    for mood in moodvies:
        dictMoodvies[mood[0]] = mood[1:] 
    return dictMoodvies

#print dictMoodvies(os.getcwd() + '\Documents\Academics\CS\\movies.txt')

#read the file, create dictionary with titles.txt that looks like this {'Titanic':[1997, 'James Cameron','Leonardo DiCaprio','Kate Winslet'],...}

def dictMovies(fileName):
    fin = open(fileName) 
    movies = []
    dictMovies = dict()     
    for line in fin:
        line = line.strip()
        movies.append(line.split(', ')) 
    for title in movies:
        dictMovies[title[0]] = title[1:] 
    return dictMovies
#print dictMovies(os.getcwd() + '\Documents\Academics\CS\\titles2.txt')

import random 
def randomize(movies): #import dictionary created from titles.txt
   i = 0
   randomMovies = []
   while i < 3:
       randomMovie = random.choice(movies)
       if randomMovie not in randomMovies:
           randomMovies.append(randomMovie)
           i = i + 1
   return randomMovies

#adds new movie to Mood dictionary (no keys added, just new values in existing keys)
def addMovieToMood(title, mood, dictMoodvies):
    for key,values in dictMoodvies.items():
        if key == mood:
            values.append(title) 
    return dictMoodvies
        
#adds new movie information to Titles dictionary (new keys and values added)
def addMovieInfo(title, year, director, actor1, actor2, dictMovies):
    if title not in dictMovies.keys():
        dictMovies[title] = [year, director, actor1, actor2]
    return dictMovies

###########################################
# Configuration
#
DEBUG = True
#SECRET_KEY = 'development key'
SECRET_KEY = 'OPENSHIFT_SECRET_TOKEN'
allMovies = dictMoodvies('static/Movies.txt')
movieData = dictMovies('static/Titles.txt')
USERNAME = 'flask'
PASSWORD = 'db'

###########################################
# Create our application
#

current_dir = os.path.dirname(os.path.abspath(__file__))
template_folder = os.path.join(current_dir, 'templates')
static = os.path.join(current_dir,'static')
app = Flask(__name__, template_folder=template_folder, static_url_path=static)
app.config.from_object(__name__)


###########################################
# Routers

@app.route('/')
def index():
    return render_template('Moodvie.html')

@app.route('/static/<filename>')
def static_files(filename):
    return app.send_static_file(filename)
    
@app.route('/movieresults/<title>')
def show_results(title):
    return render_template('Moodvie2.html',title = title,
                                movies = randomize(allMovies[title]),
                                movieData = movieData)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You are logged in')
            return redirect(url_for('index'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You are logged out')
    return redirect(url_for('index'))

def main():
    app.run(debug=True)

if __name__ == '__main__':
    main()