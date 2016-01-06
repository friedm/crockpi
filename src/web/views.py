from flask import render_template
from web import app, models
import pygal

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', target=150)

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
