from Quiz.multiplechoice import Multiplechoice
from Quiz.package import Package
from Quiz.statistics import Statistics
from data.connection import Connection
import random

# !!Nukes current data!!
for t_name in ["questions", "statistics", "packages"]:
    with Connection() as con:
        with con:
            con.execute("DROP TABLE IF EXISTS " + t_name)

# Ensures that databases are created
Multiplechoice()
Statistics()
Package()

# helper function
def gen_num():
    return str(random.randint(100, 999))

data = [
    {"Harry Potter trivia":[
        ["What was Nearly Headless Nick's last name?", "de Mimsy-Porpington", "von Grieve", "van Orton", "Delaney-Podmore"],
        ["How old was Nicholas Flamel in the Sorcerer's Stone?", "655", gen_num(), gen_num(), gen_num()],
        ["How many possible Quidditch fouls are there?", "700", gen_num(), gen_num(), gen_num()],
        ["For Harry's 17th birthday, what color did Hermione turn the leaves of the Weasley’s crabapple tree?", "Gold", "Green", "Red", "Yellow"],
        ["Where is the Slytherin common room located?", "the dungeons", "the common room", "under a tree", "in a tower"]
                            ]},
    {"History trivia": [

    ]},
    {"Random trivia": [
        ["Which letter does not appear in any US state name?", "Q", "Z", "J", "X"],
        ["'Memory' is a song featured in which musical?", "Cats", "Miss Saigon", "Les Miserables", "The Lion King"]
    ]},
    {"Philosophy trivia": [
        ["Which of these famous existentialists declined the Nobel Peace Prize for literature in 1964?", "Jean-Paul Sartre", "Martin Heidegger", "Karl Jaspers", "Claudio Abbado"],
        ["Who co-authored the Communist Manifesto with Marx?", "Friedrich Engels", "Karl Kautsky", "Vladimir Lenin", "Otto Bauer"],
        ["Who invented the study of formal logic and pioneered the study of zoology?", "Aristotle", "Socrates", "Saint Augustine", "Pythagoras"],
        ["The term 'positivism' designates the thought of which of these philosophers?", "Auguste Comte", "David Hume", "John Locke", "John Stuart Mill"],
        ["Who was Aristotle's teacher?", "Plato", "Socrates", "Epicurus", "Xenophanes"]
    ]}
]


types = ["Quiz 1", None, None,  "Quiz 2"]
counter = -1

for package in data:
    for p_name, qs in package.items():
        counter += 1
        p_id = Package.add_package(p_name)
        Package.save_package(p_id, p_name, types[counter])
        for text, correct, in1, in2, in3 in qs:
            Multiplechoice.add_question({"correct": correct, "text": text, "incorrect": [in1, in2, in3], "package_id": p_id})


