def is_even(number):
    if(number % 2 == 0):
        return True
    else:
        return False            

number = int(input("Enter a number: "))
print(is_even(number))