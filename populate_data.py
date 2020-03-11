from Quiz.multiplechoice import Multiplechoice

data = [
    ["Which letter does not appear in any US state name?", "Q", "Z", "J", "X"]
]

for text, correct, in1, in2, in3 in data:
    Multiplechoice.add_question({"correct": correct, "text": text, "incorrect": [in1, in2, in3]})
