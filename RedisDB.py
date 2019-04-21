import redis
import string
import json
import os
from flask import Flask, Response, redirect, request, render_template, session

class redisDB:
    def __init__(self):        
        self.redisClient = redis.from_url(os.environ.get('REDIS_URL') or 'redis://127.0.0.1:6379/')  
        self.application = Flask(__name__, static_url_path='')
        self.application.secret_key = os.environ.get('SECRET_KEY') or os.urandom(32) 

    def add_user_answer(self):
        question = self.redisClient.get("CurrentQuestion")    
        userName = session['name']          
        answer = request.form['name']
        self.redisClient.hset(question, userName, answer)
        self.redisClient.publish("answer-stats", "new user answer")        

        #unknown if the next two functions are needed
    def get_user_answer(self, question, userName):
        question = getCurrentQuestion()
        userName = session['name']
        return(self.redisClient.hget(question, userName))   
    
    def get_questionCount(self):         
        return self.redisClient.get("qc") 

    def store_question(self, question_string):        
        string_list = question_string.splitlines()        
        length = len(string_list)
        question = ""
        potential_answer_list = []
        question_count = 0
        for iterator in range(1, length + 2):            
            if iterator % 7 == 0 or iterator == 1:
                question = string_list[iterator -1].strip()
                question_count += 1                                
            elif iterator % 6 == 0:
                question_string = json.dumps({"question": question, "answers": potential_answer_list})
                self.redisClient.hset("Question" + str(int(iterator/6)), question_string , correct_awnser )                
                potential_answer_list.clear()
            else:
                string_line = string_list[iterator-1].strip()
                if string_line[0] == "+":
                    correct_awnser = iterator % 6 - 1                   
                potential_answer_list.append(string_line[2:])         
        self.redisClient.set("qc", question_count)           

#store sample questions
def input_questions(RDB):
    practice_string = """What is the best food in the world?
    - tacos
    + spaghetti
    - pizza
    - burger

    What is the best database in the world?
    - Microsoft Access
    - Oracle
    - Redis
    + It depends on your situation and that’s why you have to have a broad understanding of the field"""  

    RDB.store_question(practice_string)
   

RDB = redisDB()
#input_questions(RDB)
#print(RDB.get_questionCount())




    
