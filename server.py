import os
import redis
from flask import Flask

r = redis.from_url(os.environ.get("REDIS_URL"))

app = Flask(__name__)

# Used by the host to start the quiz
@app.route('/create-quiz', methods=['POST'])
def create_quiz():
	raise NotImplementedError

# Used by a client to register a name
# Returns some sort of error if name is already taken
@app.route('/set-name', methods=['POST'])
def set_name():
	raise NotImplementedError

# Used by a client to submit an answer
# Takes an answer number [1-4] and some sort of client identification
# Results in events being sent from /answer-stats
@app.route('/answer', methods=['POST'])
def answer():
	raise NotImplementedError

# Used by a client to listen for new questions
# Takes some sort of client identification
# Returns a stream of question objects and updates to the client's score
@app.route('/new-questions')
def new_questions():
	raise NotImplementedError

# Used by the host to advance to the next question
# Grades responses to the current question
# Returns the new question and an updated leaderboard
# Results in events being sent from /new-questions
@app.route('/next-question', methods=['POST'])
def next_question():
	raise NotImplementedError

# Used by the host to create a live-updating response chart
# Returns a stream of answer counts - perhaps arrays like [1,15,0,2]?
@app.route('/answer-stats')
def answer_stats():
	raise NotImplementedError
