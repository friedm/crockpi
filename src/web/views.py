from threading import Thread, Lock

from flask import render_template, redirect, request
from web import app, models
import pygal

from .forms import ControlForm

from .crockpi.controller import Controller
from database import Database

db_lock = Lock()

class ControllerThread(Thread):
    running = False
    instance = None
    data = []

    def __init__(self):
        Thread.__init__(self)
        self.controller = Controller(values=ControllerThread.data, database=Database(db_lock))

    def set_target(self, target):
        self.target = target

    def run(self):
        if ControllerThread.running:
            return

        ControllerThread.running = True
        ControllerThread.instance = self
        self.controller.run(self.target)

    def stop(self):
        print('stopping thread...')
        self.controller.stop()
        ControllerThread.running = False
        ControllerThread.instance.join()
        ControllerThread.instance = None
        ControllerThread.data = []

    def get_target(self):
        return self.target


@app.route('/')
@app.route('/index')
def index():
    target_temp = '?'
    if ControllerThread.running:
        target_temp = ControllerThread.instance.get_target()
    return render_template('index.html', target=target_temp)

@app.route('/_get_chart')
def get_chart():
    chart = pygal.XY()
    chart.title = 'Current Session'
    chart.show_legend = False
    chart.x_title = 'Seconds Since Start'
    chart.y_title = 'Temperature in Fahrenheit'
    chart.style = pygal.style.CleanStyle()
    chart.add('Temperature', shrink_datapoints(ControllerThread.data))

    return chart.render()

@app.route('/history')
def history():
    charts = []
    db_lock.acquire()
    sessions = models.ControlSession.query.order_by('time desc').limit(5).all()
    db_lock.release()

    for session in sessions:
        vals = []
        db_lock.acquire()
        session_data = models.Data.query.filter(models.Data.session_id==session.id)
        db_lock.release()
        for data in session_data:
            vals.append((data.seconds_since_start, data.value))


        charts.append(str(create_chart(session,shrink_datapoints(vals))))

    return render_template('history.html',charts=''.join(charts))


def shrink_datapoints(values):
    result = []
    if len(values) <= 100:
        return values

    for items in chunk(values, 2):
        if len(items) < 2: 
            result.extend(items)
            break
        result.append(((items[0][0] + items[1][0])/2, (items[0][1] + items[1][1])/2))

    if len(result) > 100:
        return shrink_datapoints(result)
    else:
        return result

def chunk(sequence, chunk_size):
    return (sequence[pos:pos + chunk_size] for pos in range(0, len(sequence), chunk_size))


def create_chart(session,values):
    chart = pygal.XY()
    chart.title = 'target temp ' + str(session.target_temp) + 'F ' + session.time.strftime('%m %d %Y %T')
    chart.show_legend = False
    chart.x_title = 'Seconds Since Start'
    chart.y_title = 'Temperature in Fahrenheit'
    chart.style = pygal.style.CleanStyle()
    chart.height = 500
    chart.add('Temperature', values)
    return chart.render().decode('utf-8')

@app.route('/control', methods=['GET', 'POST'])
def control():
    form = ControlForm()
    if request.method == 'POST' and form.validate():
        if ControllerThread.instance:
            ControllerThread.instance.stop()
            print('stopped controller')

        print('starting controller')
        crockpi_controller = ControllerThread()
        target_temp = form.target_temp.data
        crockpi_controller.set_target(target_temp)
        crockpi_controller.start()

        return redirect('/index')

    return render_template('control.html', form=form)

