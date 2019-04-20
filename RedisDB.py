import redis
import string

class redisDB:
    def __init__(self):
        self.questionCount = 0
        self.redisClient = redis.Redis(
            host='localhost',
            port=6379,
            password='')
    
    def getAll(self, question):
        print(self.redisClient.hgetall(question))

    def add_answer(self, question, userName, answer):
        self.redisClient.hset(question, userName, answer)        

    def get_answer(self, question, userName):
        print(self.redisClient.hget(question, userName))

    def add_scores(self, score, playerName):
        self.redisClient.zadd("players", {playerName: score})

    def print_descending(self):    
        print(self.redisClient.zrange("players", 0, -1, desc=True, withscores=True))

    #gives true of false for any potential answer of a certian question
    def get_correctness(self, quesiton, potential_answer):
        print(self.redisClient.hget(quesiton, potential_answer))

    def store_question(self, question, potential_answer, correctness):
        self.redisClient.hset(question, potential_answer, correctness)

    def parse_question(self, question_string):        
        string_list = question_string.splitlines()        
        length = len(string_list)
        question = ""
        for iterator in range(1, length + 1):            
            if iterator % 7 == 0 or iterator == 1:
                question = string_list[iterator -1].strip()
                self.questionCount += 1 
                #print(question)               
            elif iterator % 6 == 0:
                pass
            else:
                string_line = string_list[iterator-1].strip()
                correctness = string_line[0]                
                potential_answer = string_line[2:]   
                #print(potential_answer)             
                self.store_question(question, potential_answer, correctness)
      

def input_answers(RDB):
    #get question# by querying redis
    RDB.add_answer("q1", "U1", "1") #quesiton 1
    RDB.add_answer("q1", "U2", "3")
    RDB.add_answer("q1", "U3", "4")
    RDB.add_answer("q2", "U1", "3") #question 2
    RDB.add_answer("q2", "U2", "4")
    RDB.add_answer("q3", "U1", "2") #question 3
    RDB.add_answer("q3", "U2", "1")

    RDB.get_answer("q2", "U2") #print

def input_scores(RDB):
    #sorted sets
    RDB.add_scores(56, "Connor")
    RDB.add_scores(17, "Jacob")
    RDB.add_scores(14, "Nathan")
    RDB.add_scores(11, "John")

    RDB.print_descending()

#store questions
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
   

    RDB.parse_question(practice_string)
    #RDB.get_correctness("What is the best food in the world?", "spaghetti")
    #print(RDB.questionCount)

RDB = redisDB()
input_questions(RDB)
#RDB.getAll("What is the best food in the world?")
    
