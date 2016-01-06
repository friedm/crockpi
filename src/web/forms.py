from flask.ext.wtf import Form
from wtforms import FloatField
from wtforms.validators import DataRequired

class ControlForm(Form):
    target_temp = FloatField('f', validators=[DataRequired()])


