
from Quiz.hangman import Hangman
from Quiz.statistics import Statistics

# Statistics.create_answer_stats({"id": 4,
#                                 "quiz_format": 1,
#                                 "status": "incorrect",
#                                 "time": 50})
time = 0
for t in Statistics().get_overall_stats():
    time += sum(t.times)
print(time)

S