# [Cheaper Clicker]
by Team CheaperClicker (Jon Fenn, Connor Mote, Nathan Teeter, and Jacob Winters)

## [Introduction]
We will create a proof of concept for a digital classroom quizzing system, similar to kahoot.it or the clickers we have used in class. Students will use their phones to answer questions shown on a main projected display. The main display will receive live updates of student responses via server-sent events.

## [Schema]
- QuestionCount int
- CurrentQuestion int in \[1, QuestionCount]
- Scores SortedSet names->score (names are reserved by creating an entry in Scores)
- Answers{1..QuestionCount} hash name->answer (as int in \[1, 4])
- Question{1..QuestionCount} hash
  - question: json like '{"question": "What is Redis?","answers": \["A NoSQL database","A breed of dog","The best pizza topping","A flavor of ice cream"]}'
  - ans: int in \[1, 4]
