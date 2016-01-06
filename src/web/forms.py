from flask.ext.wtf import Form
from wtforms import FloatField
from wtforms.validators import DataRequired

class StartForm(Form):
    target_temp = FloatField('f', validators=[DataRequired()])

class StopForm(Form):
    pass

