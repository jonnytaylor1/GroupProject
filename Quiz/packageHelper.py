from Quiz.questions import QuestionDB
from re import search

def check_for_numbers(package_id):
    for q in QuestionDB.get_package_questions(package_id=package_id):
        for answer in q[2:]:
            if search(r"[^A-Za-z]", answer):
                return True
    return False