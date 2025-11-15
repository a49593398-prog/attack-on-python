# Armstrong number
def is_armstrong(n):
    s = str(n)
    number_digits = len(s)
    sum = 0
    for digit_char in s:
        digit = int(digit_char)
        sum += digit ** number_digits
    return sum == n

try:
    number = int(input("Enter your number: "))
    if is_armstrong(number):
        print("armstrong number")
    else:
        print("not armstrong number")
except ValueError:
    print("Invalid input. Please enter a number")
