import os
import redis
from flask import Flask, Response, redirect, request, render_template, session

r = redis.from_url(os.environ.get('REDIS_URL') or 'redis://127.0.0.1:6379/')

application = Flask(__name__, static_url_path='')
application.secret_key = os.environ.get('SECRET_KEY') or os.urandom(32)

# Used by the host to start the quiz
@application.route('/create-quiz', methods=['POST'])
def create_quiz():
	raise NotImplementedError

# Used by a client to register a name
@application.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'GET':
		return Response(render_template('login.xhtml'), mimetype='application/xhtml+xml')
	if False: # TODO this branch executes when name was already taken
		return Response(render_template('login.xhtml', error=True), mimetype='application/xhtml+xml')
	# Name wasn't taken and is now reserved for this client
	session['name'] = request.form['name']
	return redirect('/take-quiz')

@application.route('/take-quiz')
def take_quiz():
	return Response(render_template('take-quiz.xhtml'), mimetype='application/xhtml+xml')

# Used by a client to submit an answer
# Takes an answer number [1-4] and some sort of client identification
# Results in events being sent from /answer-stats
@application.route('/answer', methods=['POST'])
def answer():
	raise NotImplementedError

# Used by a client to listen for new questions
# Takes some sort of client identification
# Returns a stream of question objects and updates to the client's score
@application.route('/new-questions')
def new_questions():
	raise NotImplementedError

# Used by the host to advance to the next question
# Grades responses to the current question
# Returns the new question and an updated leaderboard
# Results in events being sent from /new-questions
@application.route('/next-question', methods=['POST'])
def next_question():
	raise NotImplementedError

# Used by the host to create a live-updating response chart
# Returns a stream of answer counts - perhaps arrays like [1,15,0,2]?
@application.route('/answer-stats')
def answer_stats():
	raise NotImplementedError
