import typing
from datetime import datetime

from flask import render_template, request, redirect

from app import app, db
from app.models import Entry, Board, Team, Round, Schedule
from app.utils import make_schedule


@app.route('/')
@app.route('/index')
def index():
    entries = Board.query.all()
    return render_template('index.html', entries=entries)


@app.route('/createSchedule01', methods=['GET', 'POST'])
def create_schedule01():
    if request.method == 'GET':
        return render_template("create_schedule01.html")
    else:
        form = request.form
        count = int(form.get("count"))
        prefix = form.get("prefix")
        teams = []
        schedule = Schedule(id=int(datetime.today().strftime('%Y%m%d')),
                            title="Schedule - " + str(datetime.today().strftime('%Y%m%d')))
        if Schedule.query.get(schedule.id) is not None:

            pass
        db.session.add(schedule)
        for idx in range(1, count + 1, 1):
            team = Team(id=int(str(schedule.id) + str(idx)), title=prefix + str(idx), schedule=schedule)
            teams.append(team)
            db.session.add(team)

        for idx, events in enumerate(make_schedule(count)):
            board = Board(schedule_id=schedule.id, title="Board - " + str(idx + 1))
            for evt in events:
                t1 = evt[0]
                t2 = evt[1]
                round = Round(title=prefix + str(t1) + " vs " + prefix + str(t2), schedule=schedule, board=board,
                              team1=teams[t1 - 1], team2=teams[t2 - 1])
                board.rounds.append(round)
                db.session.add(round)
            db.session.add(board)
        db.session.commit()
        return redirect('/schedules')


@app.route('/schedules', methods=['GET'])
def schedules():
    schedules: typing.List[Schedule] = Schedule.query.filter_by(status=1).all()
    return render_template("schedule_list.html", items=schedules)


@app.route('/boardList/<int:schedule_id>', methods=['GET'])
def boards(schedule_id=0):
    boards: typing.List[Board] = Board.query.filter_by(status=1, schedule_id=schedule_id).all()
    return render_template("board_list.html", items=boards, schedule_id=schedule_id)


@app.route('/boardDetails/<int:id>', methods=['GET'])
def schedule_details(id=0):
    board: Board = Board.query.get(id)
    return render_template('board_details.html', item=board)


@app.route('/teamList/<int:schedule_id>', methods=['GET'])
def team_list(schedule_id=0):
    teams: typing.List[Team] = Team.query.filter_by(schedule_id=schedule_id).all()
    return render_template('team_list.html', items=teams, schedule_id=schedule_id)


@app.route('/roundList/<int:schedule_id>', methods=['GET'])
def event_list(schedule_id=0):
    rounds: typing.List[Round] = Round.query.filter_by(schedule_id=schedule_id).all()
    return render_template('round_list.html', items=rounds, schedule_id=schedule_id)


@app.route('/boardRoundList/<int:schedule_id>', methods=['GET'])
def schedule_event_list(schedule_id=0):
    board = Board.query.get(schedule_id)
    rounds: typing.List[Round] = Round.query.filter_by(board=board).all()
    return render_template('board_round_list.html', items=rounds, board=board)


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
