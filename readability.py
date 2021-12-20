from cs50 import get_string
import re

text = get_string("Text: ")
punct_re = re.compile(r"[.!?]")
words = 1
letters = 0
sentences = 0

for char in text:
    if char == " ":
        words += 1
    elif punct_re.match(char):
        sentences += 1

    if char.isalpha():
        letters += 1

grade = round(0.0588 * (letters / words * 100) - 0.296 *
              (sentences / words * 100) - 15.8)
result = ""

if(grade > 16):
    result = "Grade 16+"
elif grade < 1:
    result = "Before Grade 1"
else:
    result = "Grade " + str(grade)

print(result)
