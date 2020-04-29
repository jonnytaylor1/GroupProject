
from Quiz.hangman import Hangman
from Quiz.statistics import Statistics

from Quiz.password import PasswordDB

# Statistics.create_answer_stats({"id": 4,
#                                 "quiz_format": 1,
#                                 "status": "incorrect",
#                                 "time": 50})
# time = 0
for t in Statistics().get_overall_stats():
    print(t)
#

# PasswordDB.ensure_table_exists()
# # PasswordDB.set_password("hello there")
#
# print(PasswordDB.get_password())