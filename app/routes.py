import typing
from datetime import datetime

from flask import render_template, request, redirect

from app import app, db
from app.models import Entry, Schedule, Team, Event, Game
from app.utils import make_schedule


@app.route('/')
@app.route('/index')
def index():
    entries = Schedule.query.all()
    return render_template('index.html', entries=entries)


@app.route('/createGame01', methods=['GET', 'POST'])
def create_game01():
    if request.method == 'GET':
        return render_template("create_game01.html")
    else:
        form = request.form
        count = int(form.get("count"))
        prefix = form.get("prefix")
        teams = []
        game = Game(id=int(datetime.today().strftime('%Y%m%d')),
                    title="Game - " + str(datetime.today().strftime('%Y%m%d')))
        db.session.add(game)
        for idx in range(1, count + 1, 1):
            team = Team(id=idx, title=prefix + str(idx), game=game)
            teams.append(team)
            db.session.add(team)

        for idx, events in enumerate(make_schedule(count)):
            schedule = Schedule(game_id=game.id, title="Schedule - " + str(idx + 1))
            for evt in events:
                t1 = evt[0]
                t2 = evt[1]
                event = Event(title=prefix + str(t1) + " vs " + prefix + str(t2), game=game, schedule=schedule,
                              team1=teams[t1 - 1], team2=teams[t2 - 1])
                schedule.events.append(event)
                db.session.add(event)
            db.session.add(schedule)
        db.session.commit()
        return redirect('/games')


@app.route('/createGame02', methods=['GET'])
def create_game02():
    return render_template("create_game02.html")


@app.route('/games', methods=['GET'])
def games():
    games: typing.List[Game] = Game.query.filter_by(status=1).all()
    return render_template("game_list.html", items=games)


@app.route('/scheduleList/<int:gid>', methods=['GET'])
def schedules(gid=0):
    schedules: typing.List[Schedule] = Schedule.query.filter_by(status=1, game_id=gid).all()
    return render_template("schedule_list.html", items=schedules, game_id=gid)


@app.route('/scheduleDetails/<int:id>', methods=['GET'])
def schedule_details(id=0):
    schedule: Schedule = Schedule.query.get(id)
    return render_template('schedule_details.html', item=schedule)


@app.route('/teamList/<int:gid>', methods=['GET'])
def team_list(gid=0):
    teams: typing.List[Team] = Team.query.filter_by(game_id=gid).all()
    return render_template('team_list.html', items=teams, game_id=gid)


@app.route('/eventList/<int:gid>', methods=['GET'])
def event_list(gid=0):
    events: typing.List[Event] = Event.query.filter_by(game_id=gid).all()
    return render_template('event_list.html', items=events, game_id=gid)


@app.route('/scheduleEventList/<int:sc_id>', methods=['GET'])
def event_list(sc_id=0):
    schedule = Schedule.query.get(sc_id)
    events: typing.List[Event] = Event.query.filter_by(schedule=schedule).all()
    return render_template('event_list.html', items=events, schedule=schedule)


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
