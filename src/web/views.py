import datetime

from flask import render_template, redirect, request
from web import app, models, worker, database, db_lock, crockpi
import pygal

from .forms import StartForm, StopForm

from database import Database

@app.route('/')
@app.route('/index')
def index():
    target_temp = '-'
    if worker.ControllerThread.running:
        target_temp = worker.ControllerThread.instance.get_target()
    return render_template('index.html', target=target_temp, chart=get_chart().decode('utf-8'))

sensor = crockpi.tempsensor.TempSensor()
@app.route('/_get_temp')
def get_temp():
    return '{0:.2f}'.format(sensor.read())

@app.route('/_get_chart')
def get_chart():
    if len(worker.ControllerThread.data) == 0:
        return create_chart([])

    delta_data = process_data_for_charts(worker.ControllerThread.data)
    return create_chart(delta_data)

def process_data_for_charts(values):
    start = min(values, key=lambda value: value[0])[0]
    render_data = shrink_datapoints(values)
    delta_data = list(map(lambda value: ((value[0] - start),value[1]), render_data))
    return delta_data

def create_chart(values,session=None):
    chart = pygal.TimeDeltaLine()
    if session:
        chart.title = session_string(session)
    chart.show_legend = False
    chart.x_title = 'Time'
    chart.y_title = 'Temperature'
    chart.style = pygal.style.CleanStyle()
 
    chart.add("Temperature", values)

    return chart.render()

@app.route('/_get_current_session_string')
def get_current_session_string():
    session = database.get_active_session()
    return session_string(session)

def session_string(session):
    if not session:
        return 'no session'
    return str(session.target_temp) + session.time.strftime('F %m/%d/%Y %H:%M')


chart_cache = {}
@app.route('/history')
def history():
    charts = []
    sessions = database.get_latest_sessions()

    for session in sessions:
        vals = []

        if session.id in chart_cache:
            charts.append(chart_cache[session.id])
            continue

        db_lock.acquire()
        session_data = models.Data.query.filter(models.Data.session_id==session.id)
        db_lock.release()
        for data in session_data:
            vals.append((data.time, data.value))

        chart = str(create_chart(process_data_for_charts(vals),session=session).decode('utf-8'))
        charts.append(chart)
        chart_cache[session.id] = chart

    return render_template('history.html',charts=''.join(charts))

def shrink_datapoints(values):
    result = []
    cap = 100
    if len(values) <= cap:
        return values

    for items in chunk(values, 2):
        if len(items) < 2: 
            result.extend(items)
            break
        result.append(((items[0][0] + (items[1][0]-items[0][0])/2), (items[0][1] + items[1][1])/2))

    if len(result) > cap:
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
        database.delete_active_session()
    return redirect('/control')

