from datetime import datetime

from flask import render_template, request, redirect

from app import app, db
from app.models import Entry, Game, Team, Event
from app.utils import make_schedule


@app.route('/')
@app.route('/index')
def index():
    entries = Game.query.all()
    return render_template('index.html', entries=entries)


@app.route('/createEvent01', methods=['GET', 'POST'])
def create_event01():
    if request.method == 'GET':
        return render_template("create_event01.html")
    else:
        form = request.form
        count = int(form.get("count"))
        prefix = form.get("prefix")
        teams = []
        schedules = make_schedule(count)
        game = Game(id=int(datetime.today().strftime('%Y%m%d')),
                    title="Game - " + str(datetime.today().strftime('%Y%m%d')))
        db.session.add(game)
        for idx in range(1, count + 1, 1):
            team = Team(id=idx, title=prefix + str(idx), game=game)
            teams.append(team)
            db.session.add(team)

        for events in schedules:
            for evt in events:
                t1 = evt[0]
                t2 = evt[1]
                event = Event(title=prefix + str(t1) + " vs " + prefix + str(t2), game=game, team1=teams[t1 - 1],
                      team2=teams[t2 - 1])
                db.session.add(event)
        db.session.commit()
        return render_template("create_event02.html", form)

        # title = form.get('title')
        # description = form.get('description')
        # if not title or description:
        #     entry = Entry(title=title, description=description)
        #     db.session.add(entry)
        #     db.session.commit()
        #     return redirect('/')


@app.route('/createEvent02', methods=['GET'])
def create_event02():
    return render_template("create_event02.html")


@app.route('/update/<int:id>')
def updateRoute(id):
    if not id or id != 0:
        entry = Entry.query.get(id)
        if entry:
            return render_template('update.html', entry=entry)

    return "of the jedi"


@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    if not id or id != 0:
        entry = Entry.query.get(id)
        if entry:
            form = request.form
            title = form.get('title')
            description = form.get('description')
            entry.title = title
            entry.description = description
            db.session.commit()
        return redirect('/')

    return "of the jedi"


@app.route('/delete/<int:id>')
def delete(id):
    if not id or id != 0:
        entry = Entry.query.get(id)
        if entry:
            db.session.delete(entry)
            db.session.commit()
        return redirect('/')

    return "of the jedi"


@app.route('/turn/<int:id>')
def turn(id):
    if not id or id != 0:
        entry = Entry.query.get(id)
        if entry:
            entry.status = not entry.status
            db.session.commit()
        return redirect('/')

    return "of the jedi"

# @app.errorhandler(Exception)
# def error_page(e):
#     return "of the jedi"
