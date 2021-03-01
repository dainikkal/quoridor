from flask import Flask, render_template, url_for, redirect, session
from game.Game import Game 
from datetime import datetime, timedelta
import os

app = Flask(__name__)

app.secret_key = os.urandom(64)
app.permanent_session_lifetime = timedelta(minutes=20)
games = {}
whentoremove = {}
lastminutechecked = int(datetime.now().timestamp())//60

@app.before_request
def create_session():
  if 'gameid' not in session or session['gameid'] not in games.keys():
    session['gameid'] = os.urandom(16)
    games[session['gameid']] = Game()
    whentoremove[session['gameid']] = int((datetime.now() + timedelta(minutes=25)).timestamp())
  session.modified = True
  
  global lastminutechecked
  if int(datetime.now().timestamp())//60 > lastminutechecked:
    lastminutechecked = int(datetime.now().timestamp())//60
    whentoremove[session['gameid']] = int((datetime.now() + timedelta(minutes=25)).timestamp())
    to_remove = []
    for key in whentoremove.keys(): 
      if int(datetime.now().timestamp()) > whentoremove[key]: to_remove.append(key)
    for key in to_remove:
        games.pop(key)
        whentoremove.pop(key)


@app.route("/<command>")
def action(command):  
  games[session['gameid']].execute_action(command)
  return redirect(url_for("home"))

@app.route("/")
def home():
  c = games[session['gameid']].get_classes()
  l = games[session['gameid']].get_links()
  return render_template("index.html", classes=c, links=l)


if __name__ == "__main__":
  app.run()