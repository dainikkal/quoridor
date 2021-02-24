from flask import Flask, render_template, url_for, redirect, session
from game.Game import Game 
from datetime import timedelta
import time

app = Flask(__name__)

app.secret_key = "LDh!Vdga5OdCo1D7It!#YTjWtSROj7TS%81Mz^mdVqyxv@u7BVaiuPbK6&QvUcJ@"
app.permanent_session_lifetime = timedelta(minutes=20)
games = {}

@app.before_request
def create_session():
  if 'gameid' not in session or session['gameid'] not in games.keys():
    session['gameid'] = int(time.time_ns())
    games[session['gameid']] = Game()
  session.modified = True
    

@app.route("/<command>")
def action(command):  
  games[session['gameid']].wait()
  games[session['gameid']].execute_action(command)
  return redirect(url_for("home"))

@app.route("/")
def home():
  c = games[session['gameid']].get_classes()
  l = games[session['gameid']].get_links()
  return render_template("index.html", classes=c, links=l)


if __name__ == "__main__":
  app.run()