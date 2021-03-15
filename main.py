from flask import Flask, render_template, url_for, redirect, session
from game.Game import Game
from game.helper import * 
from datetime import datetime, timedelta
import os

app = Flask(__name__)

app.secret_key = os.urandom(64)
app.permanent_session_lifetime = timedelta(minutes=20)
games = {}
whentoremove = {}
lastminutechecked = int(datetime.now().timestamp()) // 60


def futuretimestamp(x):
    """Return current time in x minutes.

    Args:
        x (int): minutes to add

    Returns:
        int: timestamp added with the input
    """
    return int((datetime.now() + timedelta(minutes=x)).timestamp())


@app.before_request
def before_request():
    """before_request updates session information taken before request."""
    if 'gameid' not in session or session['gameid'] not in games.keys():
        session['gameid'] = os.urandom(16)
        games[session['gameid']] = Game()
        whentoremove[session['gameid']] = futuretimestamp(25)
    session.modified = True

    global lastminutechecked
    if int(datetime.now().timestamp())//60 > lastminutechecked:
        lastminutechecked = int(datetime.now().timestamp()) // 60
        whentoremove[session['gameid']] = futuretimestamp(25)
        to_remove = []
        for key in whentoremove.keys():
            if int(datetime.now().timestamp()) > whentoremove[key]:
                to_remove.append(key)
        for key in to_remove:
            games.pop(key)
            whentoremove.pop(key)


@app.route("/<command>")
def action(command):
    """Call the game action given by the parameter.

    Args:
        command (string): command code for action

    Returns:
        redirect: redirect to home function
    """
    if command == "reset":
        games.pop(session['gameid'])
        whentoremove.pop(session['gameid'])
    else:
        games[session['gameid']].execute_action(command)
    return redirect(url_for("home"))


@app.route("/")
def home():
    """Render page.

    Returns:
        url: webpage to be rendered
    """
    classes = games[session['gameid']].get_classes()
    links = games[session['gameid']].get_links()
    winner = games[session['gameid']].get_winner()
    log_text = ""
    log_rows = log_text.count("\n")
    clickables = ["Clickable", 
                  "Unclickable", 
                  "Clickable", 
                  "Clickable", 
                  "Unclickable"]
    buttonhrefs = ['href="/undo"',
                   'href="/redo"',
                   'href="/load"',
                   'href=/reset',
                   'href="/randomize"']

    hrefs = [buttonhrefs[i] if clickables[i] == "Clickable" else '' 
                            for i in range(5)]

    p1walls = 10
    p2walls = 10
    p1ai = ""
    p2ai = "(AI)"
    currentplayer = ["Current",""]

    if winner != Player.Empty: 
        links = ["" for _ in range(17 * 17)]
    return render_template("game.html", 
                           classes=classes, \
                           links=links, 
                           winner=winner,
                           clickables=clickables,
                           log_rows=log_rows,
                           log_text=log_text,
                           buttonhrefs=hrefs,
                           p1walls=p1walls,
                           p2walls=p2walls,
                           p1ai=p1ai,
                           p2ai=p2ai,
                           currentplayer=currentplayer)


if __name__ == "__main__":
    app.run()
