#  prime number
number =int(input('enter a number:-'))
is_prime = True
if number == 1:
    is_prime = False
else:
    for i in range(2,number):
        if number % i == 0:
            is_prime= False
if is_prime == True:
    print('prime')
else:
    print('not a prime')