from Quiz.statistics import Statistics


Statistics.update_stats({"id": 4,
                         "corrects": 3,
                         "skips": 5,
                         "incorrects": 3,
                         "time": 33})
id, q_id, corrects, incorrects, skips, time =  Statistics.get_stats(4)

print(skips)