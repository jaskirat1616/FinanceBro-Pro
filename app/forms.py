from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length

class TickerForm(FlaskForm):
    ticker = StringField('Stock Ticker', 
                        validators=[DataRequired(), 
                                  Length(min=1, max=5)])
    submit = SubmitField('Analyze')

class AIQuestionForm(FlaskForm):
    ticker = StringField('Stock Ticker',
                         validators=[DataRequired(),
                                   Length(min=1, max=5)])
    question = TextAreaField('Your Question for the AI',
                             validators=[DataRequired()])
    submit = SubmitField('Ask AI')