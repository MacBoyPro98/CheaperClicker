import os
import threading
from flask import Flask, Response, redirect, request, render_template, session
import json

import RedisDB
from auth import requires_auth_role

redisDB = RedisDB.redisDB()

pubsub_lock = threading.Lock()
answer_stats_events = set()
next_question_events = set()

def wake(events):
	with pubsub_lock:
		for event in events:
			event.set()

pubsub = redisDB.redisClient.pubsub()
pubsub.subscribe(**{
	'answer-stats': lambda _: wake(answer_stats_events),
	'next-question': lambda _: wake(next_question_events),
})
pubsub.run_in_thread(sleep_time=1, daemon=True)

application = Flask(__name__, static_url_path='')
application.secret_key = os.environ.get('SECRET_KEY') or os.urandom(32)

create_quiz_username = 'user'
create_quiz_password = os.environ.get('CREATE_QUIZ_PASSWORD')

# Used by the host to start the quiz
@application.route('/create-quiz', methods=['GET', 'POST'])
def create_quiz():
	if not (request.authorization
			and request.authorization.username == create_quiz_username
			and request.authorization.password == create_quiz_password):
		return '401 Unauthorized', 401, {'WWW-Authenticate': 'Basic'}
	if request.method == 'GET':
		return Response(render_template('create-quiz.xhtml'), mimetype='application/xhtml+xml')
	redisDB.store_question(request.files['quiz'].read().decode('utf-8'))
	session['auth_role'] = 'host'
	return redirect('/host')

# Used by a client to register a name
@application.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'GET':
		return Response(render_template('login.xhtml'), mimetype='application/xhtml+xml')
	if not redisDB.login(request.form['name']):
		return Response(render_template('login.xhtml', error=True), mimetype='application/xhtml+xml')
	# Name wasn't taken and is now reserved for this client
	session['name'] = request.form['name']
	session['auth_role'] = 'student'
	return redirect('/take-quiz')

@application.route('/take-quiz')
@requires_auth_role('student')
def take_quiz():
	return Response(render_template('take-quiz.xhtml'), mimetype='application/xhtml+xml')

# Used by a client to submit an answer
# Takes an answer number [1-4] and some sort of client identification
# Results in events being sent from /answer-stats
@application.route('/answer', methods=['POST'])
@requires_auth_role('student')
def answer():
	redisDB.add_user_answer(session['name'], request.form['answer'])
	return '', 204

# Used by a client to listen for new questions
# Takes some sort of client identification
# Returns a stream of question objects and updates to the client's score
@application.route('/new-questions')
@requires_auth_role('student')
def new_questions():
	return Response(messageResponse(session["name"]), mimetype='text/event-stream')

def calculateMessageData(name):
	questionNum = redisDB.redisClient.get("CurrentQuestion").decode("utf-8")
	question = redisDB.redisClient.hget("Question" + questionNum, "question").decode("utf-8")
	score = redisDB.redisClient.zscore("Scores", name)
	return f'{{"question":{question},"score":{score}}}'

def messageResponse(name):
	event = threading.Event()
	with pubsub_lock:
		next_question_events.add(event)
	try:
		while True:
			event.clear()
			yield f'data:{calculateMessageData(name)}\n\n'
			event.wait()
	except GeneratorExit:
		with pubsub_lock:
			next_question_events.remove(event)

@application.route('/host')
@requires_auth_role('host')
def host():
	return Response(render_template('host.xhtml'), mimetype='application/xhtml+xml')

# Used by the host to advance to the next question
# Grades responses to the current question
# Returns the new question and an updated leaderboard
# Results in events being sent from /new-questions
@application.route('/next-question', methods=['POST'])
@requires_auth_role('host')
def next_question():
	return redisDB.next_question()

# Used by the host to create a live-updating response chart
# Returns a stream of answer counts - perhaps arrays like [1,15,0,2]?
@application.route('/answer-stats')
@requires_auth_role('host')
def answer_stats():
	return Response(responseGen(), mimetype='text/event-stream')

def calculateData():
	questionNum = redisDB.redisClient.get("CurrentQuestion").decode("utf-8")
	answers = redisDB.redisClient.hvals("Answers" + str(questionNum))

	arr = [0,0,0,0]
	for answer in answers:
		arr[int(answer.decode("utf-8")) - 1] += 1

	return json.dumps(arr)

def responseGen():
	event = threading.Event()
	with pubsub_lock:
		answer_stats_events.add(event)
		next_question_events.add(event)
	try:
		while True:
			event.clear()
			yield f'data:{calculateData()}\n\n'
			event.wait()
	except GeneratorExit:
		with pubsub_lock:
			answer_stats_events.remove(event)
			next_question_events.remove(event)
