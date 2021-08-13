from cs50 import get_string
import re

checker = re.compile(r"[0-9]+$")
while True:
    cc_num = get_string("Number: ")
    if checker.match(cc_num):
        break

other_digits = ""

for i in range(len(cc_num) - 2, -1, -2):
    other_digits += cc_num[i]

sum = 0
for i in other_digits:
    for j in str(int(i) * 2):
        sum += int(j)

for i in range(len(cc_num) - 1, -1, -2):
    sum += int(cc_num[i])

amex = re.compile(r"3(4|7)*")
masterc = re.compile(r"5[1-5]*")
visa = re.compile(r"4*")

if sum % 10 != 0:
    print("INVALID")
elif len(cc_num) < 13 or len(cc_num) > 16:
    print("INVALID")
elif amex.match(cc_num):
    print("AMEX")
elif masterc.match(cc_num):
    print("MASTERCARD")
elif visa.match(cc_num):
    print("VISA")
else:
    print("INVALID")
