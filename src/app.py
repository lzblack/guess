# -*- coding: utf-8 -*-
import random

from flask import Flask, render_template, flash, redirect, url_for, session
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
from wtforms.validators import NumberRange, DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'a string that is very hard to guess'
app.config['BOOTSTRAP_SERVE_LOCAL'] = True
bootstrap = Bootstrap(app)


@app.route('/')
def index():
    # generate a random number in 0~1000, store it into session.
    session['number'] = random.randint(0, 1000)
    session['times'] = 10
    return render_template('index.html')


@app.route('/guess', methods=['GET', 'POST'])
def guess():
    times = session['times']
    result = session.get('number')
    form = GuessNumberForm()
    if form.validate_on_submit():
        times -= 1
        session['times'] = times  # update session value
        if times == 0:
            flash('Game Over. You lost. The integer is %s.' % result, 'danger')
            return redirect(url_for('.index'))
        answer = form.number.data
        if answer > result:
            if times == 1:
                flash('Too large! This will be your last guess.', 'warning')
            else:
                flash('Too large! You still have %s times.' % times, 'warning')
        elif answer < result:
            if times == 1:
                flash('Too small! This will be your last guess.', 'info')
            else:
                flash('Too small! You still have %s times.' % times, 'info')
        else:
            flash('Congratulations! You won V(＾－＾)V', 'success')
            return redirect(url_for('.index'))
    return render_template('guess.html', form=form)


class GuessNumberForm(FlaskForm):
    number = IntegerField('Enter an integer(0~1000)', validators=[
        DataRequired('Please enter a valid integer'),
        NumberRange(0, 1000, 'This integer should be between 0 and 1000!')])
    submit = SubmitField('Submit')


if __name__ == '__main__':
    app.run()
