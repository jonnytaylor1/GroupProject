from random import shuffle

class Multiplechoice():
    def __init__(self):
        self.qbank = []
        self.qbank.append({"text": "Is right choice A?", "correct": "A", "incorrect": ["B", "C", "D"]})
    def loadQuestions(self):
        pass
    def run(self):
        while(True):
            for question in self.qbank:
                print(question["text"])
                print("Choices are:")
                choices = [question["correct"]] + question["incorrect"]
                shuffle(choices)
                for choice in choices:
                    print(choice)
                ans = input("Select Answer: ")
                print("correct" if question["correct"] == ans.upper() else f"{ans} is incorrect. Correct is {question['correct']}")

Multiplechoice().run()