from flask import Flask, request, url_for, flash, render_template, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'scott'
toolbar = DebugToolbarExtension(app)




@app.route('/')
def home():
    return render_template('index.html', survey=satisfaction_survey)

@app.route('/questions/<int:n>')
def question(n):
    if n > len(list(session['responses'])):
        n= len(list(session['responses']))
        flash('DONT SKIP QUESTIONS')
        return redirect(f'/questions/{n}')
    return render_template('question.html', idx=n, survey=satisfaction_survey)

@app.route('/answers', methods=["POST"])
def answer():
    responses = session['responses']
    responses.append(request.form['choice'])
    session['responses'] = responses
    if len(list(session['responses'])) < len(satisfaction_survey.questions):
        return redirect(f'/questions/{len(responses)}')
    else:
        flash('Thanks for taking our survey!!')
        session['has_finished'] = True
        return redirect(url_for('home'))

@app.route('/start-survey', methods=['POST'])
def set_session():
    if not session.get('has_finished', False):
        session['responses'] = []
        return redirect('/questions/0')
    else:
        flash('You have already finished this survey')
        return redirect(url_for('home'))

app.run()