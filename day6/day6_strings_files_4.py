number1=int(input("Enter first number: "))
number2=int(input("Enter second number: "))

try:
    result=number1/number2
    print("The result of division is:", result)
except ZeroDivisionError:
    print("Error: Division by zero is not allowed.") 
finally:
    print("Execution completed.")
       