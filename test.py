from Quiz.multiplechoice import get_question, save_question, Multiplechoice

print(get_question(2))
Multiplechoice.add_question({"text": "A", "correct": "A", "incorrect": ["D", "B", "C"]})
print(get_question(2))