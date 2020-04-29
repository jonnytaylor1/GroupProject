from Quiz.questions import QuestionDB
from re import search

def check_for_numbers(package_id):
    for q in QuestionDB.get_package_questions(package_id=package_id):
        if search(r"[^A-Za-z ]", q[2]):
            print(q[2])
            print(search(r"[^A-Za-z ]", q[2]))
            return True
    return False