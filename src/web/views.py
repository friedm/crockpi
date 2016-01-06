from threading import Thread

from flask import render_template, redirect, request
from web import app, models
import pygal

from .forms import ControlForm

from .crockpi.controller import Controller
from database import store_controller_session, store_data

class ControllerThread(Thread):
    running = False
    instance = None
    data = []

    def __init__(self):
        Thread.__init__(self)
        self.controller = Controller(values=ControllerThread.data, controller_started=store_controller_session,measurement_taken=store_data)

    def set_target(self, target):
        self.target = target

    def run(self):
        if ControllerThread.running:
            return

        ControllerThread.running = True
        ControllerThread.instance = self
        self.controller.run(self.target)

    def stop(self):
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
    chart.add('Temperature', ControllerThread.data)

    return chart.render()

@app.route('/history')
def history():
    charts = []
    for session in models.ControlSession.query.all():
        vals = []
        for data in models.Data.query.filter(models.Data.session_id==session.id):
            vals.append((data.seconds_since_start, data.value))

        charts.append(str(create_chart(session,vals)))

    return render_template('history.html',charts=''.join(charts))

def create_chart(session,values):
    chart = pygal.XY()
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

        crockpi_controller = ControllerThread()
        target_temp = form.target_temp.data
        crockpi_controller.set_target(target_temp)
        crockpi_controller.start()

        return redirect('/index')

    return render_template('control.html', form=form)

