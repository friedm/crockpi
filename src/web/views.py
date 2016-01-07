import datetime

from flask import render_template, redirect, request
from web import app, models, worker, database, db_lock
import pygal

from .forms import StartForm, StopForm

from database import Database

@app.route('/')
@app.route('/index')
def index():
    target_temp = '?'
    if worker.ControllerThread.running:
        target_temp = worker.ControllerThread.instance.get_target()
    return render_template('index.html', target=target_temp)

@app.route('/_get_chart')
def get_chart():
    delta_data = process_data_for_charts(worker.ControllerThread.data)
    return create_chart(delta_data)

def process_data_for_charts(values):
    start = min(values, key=lambda value: value[0])[0]
    render_data = shrink_datapoints(values)
    delta_data = list(map(lambda value: ((value[0] - start),value[1]), render_data))
    return delta_data

def create_chart(values,session=None):
    chart = pygal.TimeDeltaLine()
    chart.title = 'Current Session'
    if session:
        chart.title = str(session.target_temp) + session.time.strftime('F %m %d %Y %T')
    chart.show_legend = False
    chart.x_title = 'Time'
    chart.y_title = 'Temperature'
    chart.style = pygal.style.CleanStyle()
 
    chart.add("Temperature", values)

    return chart.render()

@app.route('/history')
def history():
    charts = []
    current_id = database.get_active_session().id
    db_lock.acquire()
    sessions = models.ControlSession.query.filter(models.ControlSession.id!=current_id).order_by('time desc').limit(5).all()
    db_lock.release()

    for session in sessions:
        vals = []
        db_lock.acquire()
        session_data = models.Data.query.filter(models.Data.session_id==session.id)
        db_lock.release()
        for data in session_data:
            vals.append((data.time, data.value))

        charts.append(str(create_chart(shrink_datapoints(process_data_for_charts(vals)),session=session).decode('utf-8')))

    return render_template('history.html',charts=''.join(charts))


def shrink_datapoints(values):
    result = []
    if len(values) <= 100:
        return values

    for items in chunk(values, 2):
        if len(items) < 2: 
            result.extend(items)
            break
        result.append(((items[0][0] + (items[1][0]-items[0][0])/2), (items[0][1] + items[1][1])/2))

    if len(result) > 100:
        return shrink_datapoints(result)
    else:
        return result

def chunk(sequence, chunk_size):
    return (sequence[pos:pos + chunk_size] for pos in range(0, len(sequence), chunk_size))

@app.route('/control', methods=['GET'])
def control():
    start_form = StartForm()
    stop_form = StopForm()
    return render_template('control.html', start_form=start_form, stop_form=stop_form)

@app.route('/_control_start', methods=['POST'])
def control_start():
    form = StartForm()
    if form.validate():
        worker.start_controller_thread(form.target_temp.data, data=[])
    
        control_session_id = database.store_controller_session(datetime.datetime.utcnow(), form.target_temp.data)
        database.delete_active_session()
        database.add_active_session(control_session_id)

        return redirect('/index')

@app.route('/_control_stop', methods=['POST'])
def control_stop():
    form = StopForm()
    if form.validate():
        worker.cleanup()
    return redirect('/control')

