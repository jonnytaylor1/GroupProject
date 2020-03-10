
from Quiz.hangman import Hangman
from Quiz.statistics import Statistics
print(Hangman.get_question())

for q in Statistics().get_overall_stats():
    print(q)