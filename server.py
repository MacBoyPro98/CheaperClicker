import os
from flask import Flask, Response, redirect, request, render_template, session
import json

import RedisDB

redisDB = RedisDB.redisDB()

application = Flask(__name__, static_url_path='')
application.secret_key = os.environ.get('SECRET_KEY') or os.urandom(32)

# Used by the host to start the quiz
@application.route('/create-quiz', methods=['GET', 'POST'])
def create_quiz():
	if request.method == 'GET':
		return Response(render_template('create-quiz.xhtml'), mimetype='application/xhtml+xml')
	redisDB.store_question(request.files['quiz'].read().decode('utf-8'))
	return redirect('/host')

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
	redisDB.add_user_answer(session['name'], request.form['answer'])
	return '', 204

# Used by a client to listen for new questions
# Takes some sort of client identification
# Returns a stream of question objects and updates to the client's score
@application.route('/new-questions')
def new_questions():
	question = '{"question": "What is Redis?","answers": ["A NoSQL database","A breed of dog","The best pizza topping","A flavor of ice cream"]}'
	score = 3
	return Response(f'data:{{"question":{question},"score":{score}}}\n\n', mimetype='text/event-stream')

@application.route('/host')
def host():
	return Response(render_template('host.xhtml'), mimetype='application/xhtml+xml')

# Used by the host to advance to the next question
# Grades responses to the current question
# Returns the new question and an updated leaderboard
# Results in events being sent from /new-questions
@application.route('/next-question', methods=['POST'])
def next_question():
	return '{"question":{"question": "What is Redis?","answers": ["A NoSQL database","A breed of dog","The best pizza topping","A flavor of ice cream"]},"leaderboard":[["Steve",3],["Bob",2],["Joe",1]]}'

# Used by the host to create a live-updating response chart
# Returns a stream of answer counts - perhaps arrays like [1,15,0,2]?
@application.route('/answer-stats')
def answer_stats():
	return Response('data:[2,17,0,1]\n\n', mimetype='text/event-stream')
