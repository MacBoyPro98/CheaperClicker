import redis
import string
import json
import os

class redisDB:    
    def __init__(self):        
        self.redisClient = redis.from_url(os.environ.get('REDIS_URL') or 'redis://127.0.0.1:6379/')       

    #get name from session['name'] and answer from request.form['name']
    def add_user_answer(self, name, answer):
        questionNum = self.redisClient.get("CurrentQuestion").decode("utf-8")
        self.redisClient.hset("Answers" + questionNum, name, answer)
        self.redisClient.publish("answer-stats", "new user answer")        

        #unknown if the next two functions are needed
    def get_user_answer(self, question, userName):
        question = getCurrentQuestion()
        userName = session['name']
        return(self.redisClient.hget(question, userName))   
    
    def get_questionCount(self):         
        return self.redisClient.get("QuestionCount") 

    def store_question(self, question_string):        
        string_list = question_string.splitlines()        
        length = len(string_list)
        question = ""
        potential_answer_list = []
        question_count = 0
        for iterator in range(1, length + 2):            
            if iterator % 7 == 0 or iterator == 1:  #this line is the question
                question = string_list[iterator -1].strip()
                question_count += 1                                
            elif iterator % 6 == 0:     # this line is blank signaling the end of a question, we go ahead and enter in the data we have 
                question_string = json.dumps({"question": question, "answers": potential_answer_list})
                self.redisClient.hset("Question" + str(int(iterator/6)), "question", question_string)
                self.redisClient.hset("Question" + str(int(iterator/6)), "ans", correct_awnser )                
                potential_answer_list.clear()
            else:       #these lines will be the potential awnsers 
                string_line = string_list[iterator-1].strip()
                if string_line[0] == "+":
                    correct_awnser = iterator % 6 - 1                   
                potential_answer_list.append(string_line[2:])         
        self.redisClient.set("QuestionCount", question_count)           
        self.redisClient.set("CurrentQuestion", 1)

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
input_questions(RDB)
#print(RDB.get_questionCount())




    
