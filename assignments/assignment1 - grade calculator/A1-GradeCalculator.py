# This calculates a grade in CS 1400 for various midterm scores.
# By Soojung Kim, 2025-8-27

# assignment & quiz & lab = 10% & 25% & 10%
name = input("Write your name: ")

assignment_score = float(input("Write your assignment score: "))
quiz_score = float(input("Write your quiz score: "))
lab_score = float(input("Write your lab score: "))

without_midterm = (10 * assignment_score + 25 * quiz_score + 10 * lab_score) / 100

for midterm_score in range (0, 101, 20):
    final_score = without_midterm + float((midterm_score * 55)) / 100
    print(name + ',', "if your average midterm exam score is", int(midterm_score), "your course percentage for CS 1400 will be", str(final_score) + '.')
